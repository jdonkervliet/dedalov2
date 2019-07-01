
import logging
from typing import Callable, Collection, Deque, Iterable, Set, Sequence, Tuple

import collections
import hdt
import local_hdt
import urishortener


class Predicate:

    @staticmethod
    def fromString(id: str):
        int_value = local_hdt.document().convert_term(id, hdt.IdentifierPosition.Predicate)
        if int_value <= 0:
            raise ValueError("{} does not exist as Predicate.".format(id))
        return Predicate(int_value)

    def __init__(self, id: int):
        self.id: int = id

    def __str__(self):
        return urishortener.shorten(local_hdt.document().convert_id(self.id, hdt.IdentifierPosition.Predicate))

    def __eq__(self, other):
        return type(other) == Predicate and self.id == other.id

    def __hash__(self):
        return self.id


class Subject:

    @staticmethod
    def fromString(id: str) -> 'Subject':
        int_value = local_hdt.document().convert_term(id, hdt.IdentifierPosition.Subject)
        if int_value <= 0:
            raise ValueError("{} does not exist as Subject.".format(id))
        return Subject(int_value)

    def __init__(self, id: int):
        self.id = id

    def follow(self, predicates: Sequence[Predicate], stop_condition: Callable[[Set['Object']], bool] = lambda _: False) -> Set['Object']:
        return set(Object(o_id) for o_id in self._follow([p.id for p in predicates]))

    def _follow(self, predicates: Sequence[int]) -> Set[int]:
        document = local_hdt.document()
        to_follow: Deque[Tuple[int, Sequence[int]]] = collections.deque()
        if len(predicates) > 0:
            to_follow.append((self.id, predicates))
        res: Set[int] = set()
        while len(to_follow) > 0:
            s_id, p_ids = to_follow.pop()
            triples, _ = document.search_triples_ids(s_id, p_ids[0], 0)
            for _, _, o_id in triples:
                if len(p_ids) > 1:
                    vertex_string = local_hdt.document().convert_id(o_id, hdt.IdentifierPosition.Object)
                    new_s_id = local_hdt.document().convert_term(vertex_string, hdt.IdentifierPosition.Subject)
                    if new_s_id > 0:
                        to_follow.append((new_s_id, p_ids[1:]))
                else:
                    res.add(o_id)
        return res

    def toObject(self) -> 'Object':
        vertex_string = local_hdt.document().convert_id(self.id, hdt.IdentifierPosition.Subject)
        object_id = local_hdt.document().convert_term(vertex_string, hdt.IdentifierPosition.Object)
        if object_id <= 0:
            raise ValueError("{} does not exist as a subject.".format(vertex_string))
        return Object(object_id)

    def __str__(self):
        return urishortener.shorten(local_hdt.document().convert_id(self.id, hdt.IdentifierPosition.Subject))

    def __eq__(self, other):
        return type(other) == Subject and self.id == other.id

    def __hash__(self):
        return self.id

class Object:

    @staticmethod
    def fromString(id: str) -> 'Object':
        int_value = local_hdt.document().convert_term(id, hdt.IdentifierPosition.Object)
        if int_value <= 0:
            raise ValueError("{} does not exist as Object.".format(id))
        return Object(int_value)

    def __init__(self, id: int):
        self.id = id

    def toSubject(self) -> 'Subject':
        vertex_string = local_hdt.document().convert_id(self.id, hdt.IdentifierPosition.Object)
        subject_id = local_hdt.document().convert_term(vertex_string, hdt.IdentifierPosition.Subject)
        if subject_id <= 0:
            raise ValueError("{} does not exist as a subject.".format(vertex_string))
        return Subject(subject_id)

    def __str__(self):
        return urishortener.shorten(local_hdt.document().convert_id(self.id, hdt.IdentifierPosition.Object))

    def __eq__(self, other):
        return type(other) == Object and self.id == other.id

    def __hash__(self):
        return self.id

def objects_to_subjects(objects: Collection[Object]) -> Collection[Subject]:
    res = []
    for o in objects:
        try:
            res.append(o.toSubject())
        except ValueError:
            pass
    return res
