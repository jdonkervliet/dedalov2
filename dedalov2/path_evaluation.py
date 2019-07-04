
import logging
import math
from typing import Callable, Dict, Optional, Set

from example import Examples
from path import Path
from path_pruner import PathPruner


def find_best_path(heuristic: str, paths: Dict[Path, Path], examples: Examples, pruner: PathPruner, max_length: float = float('inf')) -> Optional[Path]:
    """Get the best path from a collection of paths.
    
    Arguments:
        paths -- A collection of paths.
        examples -- The set of examples, both positive and negative.
    
    Returns:
        Path -- The best path.
    """
    logging.info("EVALUATING {} POSSIBLE PATHS".format(len(paths)))
    score = float('-inf')
    res: Optional[Path] = None
    heuristic_search_func = get_heuristic_from_string(heuristic)
    paths_to_delete: Set[Path] = set()
    pruned: int = 0
    too_long: int = 0
    for path in paths:
        if len(path) > max_length:
            paths_to_delete.add(path)
            too_long += 1
            continue
        if pruner(path):
            paths_to_delete.add(path)
            pruned += 1
            continue

        new_score = heuristic_search_func(path, examples)
        if new_score > score:
            score = new_score
            res = path
    for path in paths_to_delete:
        paths.pop(path, None)
    logging.info("PRUNED {} PATHS".format(pruned))
    logging.info("REMOVED {} TOO LONG PATHS".format(too_long))
    logging.info("NEXT ROUND HAS {} REMAINING PATHS".format(len(paths)))
    return res


def entropy(p: Path, examples: Examples) -> float:
    """Metric to calculate the quality of a path. A good path should lead to good explanations.
    
    Arguments:
        p {Path} -- The path to evaluate.
        num_examples {int} -- Sum of positive and negative examples given in the input.
    
    Returns:
        float -- A numerical value representing the quality of the path. Higher is better.
    """
    res: float = 0
    for obj in p.get_end_points():
        num_roots = len(p.get_starting_points_connected_to_endpoint(obj))
        frac = num_roots/len(examples)
        assert frac >= 0
        assert frac <= 1
        res -= frac * math.log10(frac)
    return res


def shortest_path(p: Path, examples: Examples) -> float:
    return -float(len(p))


def longest_path(p: Path, examples: Examples) -> float:
    return float(len(p))

# def unified(p: Path, examples: Examples) -> float:
#     """Metric to calculate the quality of a path. A good path should lead to good explanations.
    
#     Arguments:
#         p {Path} -- The path to evaluate.
#         positives -- A set of positive examples.
    
#     Returns:
#         float -- A numerical value representing the quality of the path. Higher is better.
#     """
#     res = 0
#     for v in p.get_values():
#         e = Explanation(p, v)
#         res += evaluate_explanation(e, examples)
#     return res


HEURISTIC_NAMES: Dict[str, Callable[[Path, Examples], float]] = {
    "bfs": shortest_path,
    "entropy": entropy,
    "lpf": longest_path,
}


def get_heuristic_from_string(name: str) -> Callable[[Path, Examples], float]:
    assert name in HEURISTIC_NAMES, "Unknown search heuristic: {}.".format(name)
    return HEURISTIC_NAMES[name]
