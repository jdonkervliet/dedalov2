
import logging
from typing import Callable

MemoryProfiler = Callable[[], None]

def profiler(profile: bool) -> MemoryProfiler:
    if profile:
        from mem_top import mem_top
        def p():
            logging.debug(mem_top())
        return p
    else:
        def p():
            pass
        return p
