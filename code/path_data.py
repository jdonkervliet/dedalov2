
import atexit
import collections
import msgpack
import os
import random
import shutil
import tempfile
from typing import Dict, List, Optional, Set

from example import Example, Examples
from knowledge_graph import Object
from path import Path

DIR_NAME_SUFFIX = ".path-data-"
dir_name: str

class PathData:
    def __init__(self, path: Path, o_to_e: Dict[Example, Set[Object]], e_to_o: Dict[Object, Set[Example]]):
        self.path = path
        self.objects_to_example: Dict[Example, Set[Object]] = o_to_e
        self.examples_to_object: Dict[Object, Set[Example]] = e_to_o

cache_size = float('inf')
cache: Dict[Path, PathData] = collections.OrderedDict() # OrderedDict is needed for FIFO .popitem() (see _write_to_cache)

def init():
    global dir_name
    dir_name = tempfile.mkdtemp(prefix=DIR_NAME_SUFFIX, dir=".")
    atexit.register(cleanup)

def cleanup():
    shutil.rmtree(dir_name, ignore_errors=True)

def _get_file_name(p: Path) -> str:
    return os.path.abspath(os.path.join(dir_name, "-".join("empty-path" if p.edges is None else map(lambda e: str(e.id), p.edges))))

def _to_storage(pd: PathData) -> None:
    file_name = _get_file_name(pd.path)
    with open(file_name, "wb") as f:
        msgpack.dump(pd, f)

def _from_storage(p: Path) -> Optional[PathData]:
    file_name = _get_file_name(p)
    if os.path.isfile(file_name):
        with open(file_name, "rb") as f:
            return msgpack.load(f)
    return None

def _write_to_cache(pd: PathData) -> None:
    if len(cache) >= cache_size:
        item = cache.popitem()[1]
        _to_storage(item)
    cache[pd.path] = pd

def _store(pd: PathData) -> None:
    _write_to_cache(pd)

def _load(p: Path) -> Optional[PathData]:
    if p in cache:
        return cache[p]
    return _from_storage(p)

def _data(p: Path, examples: Examples) -> PathData:
    objects_to_example: Dict[Example, Set[Object]] = {}
    examples_to_object: Dict[Object, Set[Example]] = {}
    res: PathData = PathData(p, objects_to_example, examples_to_object)
    for e in examples:
        objects_reachable_via_example = e.subject.follow([] if p.edges is None else [ p for p in p.edges ])
        objects_to_example[e] = objects_reachable_via_example
        for o in objects_reachable_via_example:
            examples_to_object.setdefault(o, set()).add(e)
    return res

def _load_or_compute(p: Path, examples: Examples) -> PathData:
    pd: Optional[PathData] = _load(p)
    if pd is None:
        pd = _data(p, examples)
        _store(pd)
    return pd

def connected_examples(examples: Examples, path: Path) -> Set[Example]:
    pd: PathData = _load_or_compute(path, examples)
    return set(pd.objects_to_example.keys())

def connected_examples_to_object(examples: Examples, path: Path, o: Object) -> Set[Example]:
    pd: PathData = _load_or_compute(path, examples)
    return pd.examples_to_object[o]

def connected_objects(examples: Examples, path: Path) -> Set[Object]:
    pd: PathData = _load_or_compute(path, examples)
    return set(pd.examples_to_object.keys())
