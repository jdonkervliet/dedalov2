
import logging
import os
from typing import Optional

import hdt

doc: Optional[hdt.HDTDocument]

def init(hdt_file_path: str):
    if not os.path.isfile(hdt_file_path):
        raise ValueError("{} is not a valid HDT file.".format(hdt_file_path))
    logging.info("Loading LOD-a-lot file.")
    global doc
    doc = hdt.HDTDocument(hdt_file_path)
    logging.info("Loaded LOD-a-lot file.")

def document() -> hdt.HDTDocument:
    if doc is None:
        raise ValueError("HDT Document not initialized.")
    return doc