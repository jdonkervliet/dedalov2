
import bisect
from typing import Collection, Set, Tuple

import path_data
from example import Example, Examples
from explanation import Explanation, Record
from knowledge_graph import Subject
from path import Path


def find_best_explanation(explanations: Set[Explanation], examples: Examples) -> None:
    """Find the best explanations out of a large collection.
    
    Arguments:
        explanations -- A (potentially large) collection of explanations.
        examples -- The set of examples, both positive and negative.
    
    Returns:
        Summary -- A summary of the best explanations.
    """
    for e in explanations:
        new_score = evaluate_explanation(e, examples)
        roots = e.explains(examples)
        positive_example_set = set(examples.positives)
        r = Record(e, new_score, num_examples=len(examples), num_positives=len(examples.positives), num_connected_positives=ftp(roots, positive_example_set), num_connected_negatives=ffp(roots, positive_example_set))
        e.record = r
        e.path.max_score_found_on_path = max(e.path.max_score_found_on_path, new_score)

# TODO use _fuzzy (underscore) to allow reusing found roots.
def evaluate_explanation(e: Explanation, examples: Examples) -> float:
    """Evaluate the quality of an explanation.
    
    Arguments:
        e {Explanation} -- To compute the quality of.
    
    Returns:
        float -- A numeric value for the quality of the explanation. Higher is better.
    """
    return fuzzy_f_measure(e, examples)

def fuzzy_f_measure(e: Explanation, examples: Examples) -> float:
    """Calculates the F-measure score.
    Returns 0 if the denominator is 0 to avoid division by zero.
    
    Arguments:
        roots {set} -- The roots explained by some explanation.
        positives {set} -- The positive examples
    
    Returns:
        float -- the F-measure value
    """
    return _fuzzy_f_measure(e.explains(examples), examples)

def max_fuzzy_f_measure(p: Path, examples: Examples) -> float:
    return _fuzzy_f_measure(set(e for e in path_data.connected_examples(examples, p) if e.positive), examples)

def _fuzzy_f_measure(roots: Set[Example], examples: Examples) -> float:
    ftp_value, ffp_value, ffn_value = _tfpn_roots_positives(roots, set(examples.positives))
    fp_value = fp(ftp_value, ffp_value)
    fr_value = fr(ftp_value, ffn_value)
    if fp_value + fr_value == 0:
        return 0.0
    res = 2 * (fp_value*fr_value)/(fp_value+fr_value)
    return res

# def jesses_fuzzy_measure(roots: Collection[Example], positives: Collection[Subject]) -> float:
#     ftp_value = ftp(roots, positives)
#     good = ftp_value / len(positives)
#     ffp_value = ffp(roots, positives)
#     bad = ffp_value / (len(examples) - len(positives))
#     res = good - bad
#     assert res >= -1
#     assert res <= 1
#     return res

def ffp(roots: Set[Example], positives: Set[Example]) -> int:
    """Calculates the number of false positives for the given explanation and positive examples.
    
    Arguments:
        e {Explanation} -- The explanation to compute the false positives for.
        positives -- A set of positive examples.
    
    Returns:
        float -- The number of false positives.
    """
    return len(roots - positives)

def ffn(roots: Set[Example], positives: Set[Example]) -> int:
    """Calculates the number of false negatives for the given explanation and positive examples.
    
    Arguments:
        e {Explanation} -- The explanation to compute the false negatives for.
        positives -- A set of positive examples.
    
    Returns:
        float -- The number of false negatives.
    """
    return len(positives - roots)

def ftp(roots: Set[Example], positives: Set[Example]) -> int:
    """Calculates the number of true positives for the given explanation and positive examples.
    
    Arguments:
        e {Explanation} -- The explanation to compute the true positives for.
        positives -- A set of positive examples.
    
    Returns:
        float -- The number of true positives.
    """
    return len(roots & positives)

def fr(ftp_value: float, ffn_value: float) -> float:
    """Calculates the recall value using the true positives and the false negatives.
    Returns 0 if the denominator is 0 to avoid division by zero.
    
    Arguments:
        ftp_value {float} -- Number of fuzzy true positives.
        ffn_value {float} -- Number of fuzzy false negatives.
    
    Returns:
        float -- The fr value.
    """
    if ftp_value == 0:
        return 0.0
    return ftp_value / (ftp_value + ffn_value)

def fp(ftp_value: float, ffp_value: float) -> float:
    """Calculates precision value using the true positives and the false positives.
    Returns 0 if the denominator is 0 to avoid division by zero.
    
    Arguments:
        ftp_value {float} -- Number of fuzzy true positives.
        ffp_value {float} -- Number of fuzzy false positives.
    
    Returns:
        float -- The fp value.
    """
    if ftp_value == 0:
        return 0.0
    return ftp_value / (ftp_value + ffp_value)

def tfpn(e: Explanation, examples: Examples) -> Tuple[float, float, float]:
    """Computes the true positives, false positives, and false negatives of an explanation.
    Computing them all at once saves a little bit of computation time.
    
    Arguments:
        e {Explanation} -- The explanation to compute the tp, fp, and fn for.
        positives -- A set of positive examples.
    
    Returns:
        (float, float, float) -- A three-tuple of floats holding the true positives, false positives, and false negatives respectively.
    """
    roots = e.explains(examples)
    return _tfpn_roots_positives(roots, set(examples.positives))

def _tfpn_roots_positives(roots: Set[Example], positives: Set[Example]) -> Tuple[float, float, float]:
    tp = ftp(roots, positives)
    fp = ffp(roots, positives)
    fn = ffn(roots, positives)
    return (tp, fp, fn)
