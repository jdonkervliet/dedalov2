
import copy
from typing import Callable, Collection, Dict, List, MutableSet, Optional, Set

from example import Example, Examples
from knowledge_graph import Object, Predicate, Subject
from linked_list import LinkedNode

# Todo implement Paths class, remove the need to pass 'paths' to extend.
class Path:

    def __init__(self, edges: Optional[LinkedNode]):
        self.edges: Optional[LinkedNode] = edges
        # TODO figure out what to do with this field.
        self.max_score_found_on_path: float = 0
        self.objects_to_subject: Dict[Subject, Set[Object]] = {}
        self.subjects_to_object: Dict[Object, Set[Subject]] = {}

    def extend(self, paths: Dict['Path','Path'], s: Subject, p: Predicate, o: Object) -> 'Path':
        edges = LinkedNode(p, self.edges)
        path = Path(edges)
        if path in paths:
            path = paths[path]
        else:
            paths[path] = path
        if len(path) == 1:
            path.objects_to_subject.setdefault(s, set()).add(o)
            path.subjects_to_object.setdefault(o, set()).add(s)
        else:
            starting_points: Set[Subject] = self.subjects_to_object[s.toObject()]
            path.subjects_to_object.setdefault(o, set()).update(starting_points)
            for s in starting_points:
                path.objects_to_subject.setdefault(s, set()).add(o)
        return path

    def starting_points(self) -> Set[Subject]:
        return set(self.objects_to_subject.keys())

    def starting_points_connected_to_object(self, o: Object) -> Set[Subject]:
        return self.subjects_to_object.get(o, set())

    def end_points(self) -> Set[Object]:
        return set(self.subjects_to_object.keys())

    def __len__(self):
        if self.edges is None:
            return 0
        return len(self.edges)

    def __hash__(self):
        return hash(self.edges)

    def __eq__(self, other):
        return self.edges == other.edges

    def __str__(self):
        if self.edges is None:
            return ""
        return " -> ".join(map(lambda e: str(e), self.edges))
