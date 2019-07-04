
import os
import path
from typing import Optional, Set

class Blacklist:

    @staticmethod
    def fromFile(filename: Optional[str]) -> 'Blacklist':
        bl = Blacklist()
        if filename is not None:
            if not os.path.isfile(filename):
                raise ValueError("{} is not a file!".format(filename))
            with open(filename) as fin:
                lines = map(lambda line: line.strip(), fin.readline())
                for line in lines:
                    bl.addToBlacklist(line)
        return bl

    def __init__(self):
        self.blacklisted_items: Set[str] = set()

    def addToBlacklist(self, item: str) -> None:
        self.blacklisted_items.add(item)

    def isBlacklisted(self, string: str) -> bool:
        return string.strip() in self.blacklisted_items
