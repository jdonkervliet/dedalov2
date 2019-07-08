
import logging
from typing import Callable, Collection

from .example import Examples
from .path import Path

PathPruner = Callable[[Path], bool]

LOG = logging.getLogger('dedalov2.path_pruner')


def prune_max_path_score_greater_equal(explanation_evaluation_func: Callable[[Path, Examples], float], examples: Examples) -> PathPruner:
    def p(p: Path) -> bool:
        new_max = explanation_evaluation_func(p, examples)
        best_found = p.max_score_found_on_path
        should_prune = best_found >= new_max
        if should_prune:
            return True
        return False
    return p


def prune_max_path_score_greater(explanation_evaluation_func: Callable[[Path, Examples], float], examples: Examples) -> PathPruner:
    def p(p: Path) -> bool:
        new_max = explanation_evaluation_func(p, examples)
        best_found = p.max_score_found_on_path
        should_prune = best_found > new_max
        if should_prune:
            return True
        return False
    return p


def prune_max_score_greater_equal(explanation_evaluation_func: Callable[[Path, Examples], float], examples: Examples) -> PathPruner:
    max_score: float = 0.0

    def p(p: Path) -> bool:
        nonlocal max_score
        new_max = explanation_evaluation_func(p, examples)
        should_prune = max_score >= new_max
        if should_prune:
            return True
        else:
            max_score = new_max
            return False
    return p


def prune_max_score_greater(explanation_evaluation_func: Callable[[Path, Examples], float], examples: Examples) -> PathPruner:
    max_score: float = 0.0

    def p(p: Path) -> bool:
        nonlocal max_score
        new_max = explanation_evaluation_func(p, examples)
        should_prune = max_score > new_max
        if should_prune:
            return True
        else:
            max_score = new_max
            return False
    return p


def prune_multi_pruner(pruners: Collection[PathPruner], examples: Examples) -> PathPruner:
    def p(p: Path) -> bool:
        for pruner in pruners:
            if pruner(p):
                return True
        return False
    return p


PATH_PRUNER_NAMES = {
    "maxge": prune_max_score_greater_equal,
    "maxg": prune_max_score_greater,
    "pathge": prune_max_path_score_greater_equal,
    "pathg": prune_max_path_score_greater,
}
