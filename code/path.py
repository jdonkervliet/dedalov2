
import copy
from typing import Callable, Collection, Dict, List, MutableSet, Optional, Set

from example import Example, Examples
from knowledge_graph import Object, Predicate, Subject
from linked_list import LinkedNode


class Path:

    def __init__(self, edges: Optional[LinkedNode]):
        self.edges: Optional[LinkedNode] = edges
        self.max_score_found_on_path: float = 0

    def extend(self, paths: Dict['Path','Path'], s: Subject, p: Predicate, o: Object) -> 'Path':
        edges = LinkedNode(p, self.edges)
        path = Path(edges)
        if path in paths:
            path = paths[path]
        else:
            paths[path] = path
        return path

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
