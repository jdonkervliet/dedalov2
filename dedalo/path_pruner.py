
import logging
from typing import Callable, Collection, Dict

import explanation_evaluation
from example import Example, Examples
from explanation import Explanation
from path import Path

PathPruner = Callable[[Path], bool]

def prune_max_path_score(explanation_evaluation_func: Callable[[Path, Examples], float], examples: Examples) -> PathPruner:
    def p(p: Path) -> bool:
        new_max = explanation_evaluation_func(p, examples)
        best_found = p.max_score_found_on_path
        should_prune = best_found >= new_max
        if should_prune:
            logging.debug("SKIP {} FOUND {} MAX {}".format(p, best_found, new_max))
            return True
        return False
    return p

def prune_multi_pruner(pruners: Collection[PathPruner], examples: Examples) -> PathPruner:
    def p(p: Path) -> bool:
        for pruner in pruners:
            if pruner(p):
                return True
        return False
    return p
