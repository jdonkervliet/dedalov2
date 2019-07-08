#!/usr/bin/env python

import argparse
import codecs
import gc
import logging
import math
import os
import subprocess
import sys
import time
from typing import Dict, Collection, Iterator, List, Optional, Set, Tuple

import psutil

from . import explanation_evaluation
from . import local_hdt
from . import path_evaluation
from . import path_pruner
from . import urishortener
from .blacklist import Blacklist
from .example import Examples
from .explanation import Explanation
from .knowledge_graph import Predicate, Vertex
from .memory_profiler import MemoryProfiler, profiler
from .path import Path
from .path_evaluation import HEURISTIC_NAMES
from .path_pruner import PathPruner


def strict_handler(exception):
    return u"", exception.end


codecs.register_error("strict", strict_handler)
LOG = logging.getLogger('dedalov2.ddl')

def validate_search_heuristic(heuristic: str) -> None:
    path_evaluation.get_heuristic_from_string(heuristic)


def print_examples(examples: Examples) -> None:
    LOG.debug("Using examples:")
    for e in examples:
        LOG.debug(e)


def print_git_hash() -> None:
    dedalov2_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    cmd = subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dedalov2_directory)
    if cmd.returncode == 0:
        commit_hash = cmd.stdout.decode('UTF-8').strip()
        LOG.debug("Dedalov2 repository is currently at commit {}".format(commit_hash))
    else:
        LOG.warning("Dedalov2 not located in git repository.")


def mem_limit_exceeded(process: psutil.Process, memlimit: float) -> Tuple[bool, float]:
    membytes = process.memory_info().rss
    if membytes >= memlimit:
        gc.collect()
        membytes = process.memory_info().rss
        if membytes > memlimit:
            return (True, membytes)
    return (False, membytes)


def explain(hdt_file: str, example_file: str, output_file: str, heuristic: str, groupid: str = None, prefix: str = None,
            blacklist: str = None, truncate: int = 0, balance: bool = False, prune: int = 0, mem_profile: bool = False, **kwargs) -> None:
    """Search for an explanation given a file of URIs and the groups they belong to.
    
    Arguments:
        args -- Arguments passed by argparse.
    """
    print_git_hash()
    local_hdt.init(hdt_file)

    urishortener.setPrefixMapFromFile(prefix)
    bl = Blacklist.fromFile(blacklist)
    validate_search_heuristic(heuristic)

    examples = Examples.fromCSV(example_file, groupid=groupid, truncate=truncate, balance=balance)
    print_examples(examples)

    pruners: List[PathPruner] = []
    if prune > 0:
        pruners.append(path_pruner.prune_max_path_score(explanation_evaluation.max_fuzzy_f_measure, examples))
    pruner = path_pruner.prune_multi_pruner(pruners, examples)

    mp: MemoryProfiler = profiler(mem_profile)

    _explain(examples, output_file, heuristic, pruner, mp, blacklist=bl, **kwargs)


def _explain(examples: Examples, outputfile: str, heuristic: str,
             pruner: PathPruner, mp: MemoryProfiler, runtime: float = math.inf,
             rounds: float = math.inf, blacklist: Blacklist = None, complete: int = 0,
             minimum_score: int = -1, memlimit: float = math.inf) -> Iterator[Explanation]:
    """Search for an explanations that explains the given examples.
    
    Arguments:
        examples {Examples} -- The examples to explain.
        runtime {float} -- The maximum allowed runtime.
    
    Keyword Arguments:
        rounds {float} -- The maximum number of rounds the algorithm will run. (default: {math.inf})
    """

    nodes: Collection[Vertex] = [example.vertex for example in examples]

    paths: Dict[Path, Path] = dict()
    explanations: int = 0

    best_path: Optional[Path] = Path.from_examples(examples)
    end_time = time.time() + runtime
    round_number = 1
    shortest_path: int = 0
    process = psutil.Process(os.getpid())
    try:
        while best_path is not None and time.time() < end_time and round_number <= rounds and (complete == 0 or shortest_path < complete):
            mp()
            new_explanations: Set[Explanation] = set()
            if complete > 0 and len(best_path) < complete:
                LOG.debug("ROUND: {}".format(round_number))
                LOG.debug("PATH: {} NUMVERTICES: {}".format(best_path, len(nodes)))
                round_start = time.time()
                for i, node in enumerate(nodes):
                    _print_progress(len(nodes), i, round_number)
                    e = follow_outgoing_links(node, best_path, paths, end_time, examples, blacklist=blacklist)
                    new_explanations.update(e)
                    explanations += len(e)
                    curtime = time.time()
                    if curtime > end_time:
                        LOG.debug("RUNTIME LIMIT EXCEEDED: {} > {}. EXITING".format(curtime, end_time))
                        break
            if len(new_explanations) > 0:
                explanation_evaluation.find_best_explanation(new_explanations, examples)
                for exp in new_explanations:
                    if exp.record is not None and exp.record.score > minimum_score:
                        yield exp
            paths.pop(best_path, None)

            round_duration = time.time() - round_start
            exceeded, num_bytes = mem_limit_exceeded(process, memlimit)
            LOG.debug("ROUND: {} TIME: {} MEMBYTES: {}".format(round_number, round_duration, num_bytes))
            mp()
            round_number += 1
            if exceeded:
                LOG.debug("MEMLIMIT EXCEEDED: {} > {}. EXITING".format(num_bytes, memlimit))
                break

            if len(paths) > 0:
                if complete > 0:
                    shortest_path = min(map(lambda x: len(x), paths))
                best_path = path_evaluation.find_best_path(heuristic, paths, examples, pruner, max_length=complete - 1)
                if best_path is None:
                    break
                nodes = set(v for v in best_path.get_end_points() if v.is_subject())
            else:
                break

    except KeyboardInterrupt:
        pass
    LOG.debug("Exiting...")
    LOG.debug("Num explanations created: {}".format(explanations))


def _print_progress(number_of_nodes: int, current_node_index: int, round_number: int) -> None:
    if number_of_nodes > 10000 and current_node_index % 1000 == 0:
        LOG.debug("Round {} at {}%".format(round_number, int(current_node_index/number_of_nodes*100)))


def follow_outgoing_links(node: Vertex, best_path: Path, paths: Dict[Path, Path], end_time: float,
                          examples: Examples, blacklist: Blacklist = None) -> Set[Explanation]:
    """Follow the outgoing links of a single vertex and create new paths and explanations based on these extensions.
    
    Arguments:
        document -- HDT document.
        node {str} -- A URI / vertex in a knowledge graph.
        best_path {Path} -- The best path. Leads to this node.
        paths {dict} -- A dictionary of paths. This single hashmap is updated inside this function. Keeps track of all explored paths.
        explanations {set} -- A set of explanations. This single set is updated inside this function. Keeps track of all explored explanations.
        end_time {float} -- A wall-time value that indicates when to abort iterating over outgonig nodes.
    
    Returns:
        int -- The number of new explanations created. This value may include duplicates.
    """
    new_explanations: Set[Explanation] = set()
    triples, k = local_hdt.document().search_triples_ids(node.s_id, 0, 0)
    for s_id, p_id, o_id in triples:
        s = Vertex.fromSubjectId(s_id)
        p = Predicate(p_id)
        o = Vertex.fromObjectId(o_id)
        # Create new path.
        if blacklist is not None and blacklist.isBlacklisted(str(p)):
            continue
        path = best_path.extend(paths, s, p, o)
        exp = Explanation(path, o)
        new_explanations.add(exp)
        if time.time() > end_time:
            break
    return new_explanations


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("example_file")
    parser.add_argument("output_file", type=str, help="Output file.")
    parser.add_argument("--hdt-file", type=str, default="/scratch/wbeek/data/LOD-a-lot/data.hdt", help="Location of HDT file to use.")
    parser.add_argument("--groupid", type=int, help="The positive examples group number.")
    parser.add_argument("--truncate", "-t", type=int, help="Selects the first x positive and negative examples. The resulting input has size 2x.")
    parser.add_argument("--balance", "-b", action="store_true", help="Makes sure that the number of positive examples equals the number of negative examples. \
        Is performed after the _truncate_ option.")

    parser.add_argument("--heuristic", type=str, choices=HEURISTIC_NAMES, default="bfs", help="The search heuristic to use.")

    parser.add_argument("--complete", "-c", type=int, default=0, help="Perform a complete search of all paths up to given length.")
    parser.add_argument("--runtime", type=float, default=math.inf, help="Number of seconds the program is allowed to run.")
    parser.add_argument("--rounds", default=math.inf, help="Number of rounds the program is allowed to run.")
    parser.add_argument("--memlimit", type=int, default=2**35, help="Stops the program once it uses more than the given amount of RAM in bytes.")

    parser.add_argument("--prefix", type=str, help="File containing URI prefixes. Two columns [abbrv prefix] separated by whitespace.")
    parser.add_argument("--blacklist", type=str, help="File containing blacklisted URIs. The program does not follow these links.")

    parser.add_argument("--prune", "-p", type=int, default=0, help="How aggressively to prune the search space. Higher values indicate more pruning.")
    parser.add_argument("--minimum_score", type=float, default=-1, help="Explanations with scores less or equal to given value are not printed.")

    parser.add_argument("--mem-profile", action="store_true", help="Occassionally log memory usage. Can help with finding memory leaks.")
    args = parser.parse_args()

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S'))
    logging.getLogger('').addHandler(ch)

    if os.path.isfile(args.output_file):
        print("Output file {} already exists. Exiting.".format(args.output_file))
        sys.exit(0)

    fh = logging.FileHandler(args.output_file)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S'))
    logging.getLogger('').addHandler(fh)

    logging.getLogger().setLevel(logging.DEBUG)

    args_dict = vars(args)
    for k, v in args_dict.items():
        logging.info("USING {}: {}.".format(k.upper(), v))
    explain(**args_dict)
