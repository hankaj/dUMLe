from enum import Enum, auto
from typing import List


class Mode(Enum):
    """
    dosc for Mode
    """
    ALL = auto()
    BRIEF = auto()


class OutputGenerator:
    """ docs for OutputGenerator"""

    def __init__(self):
        diagrams = {}

    def generate(self, diag_name: str, mode: Mode, object_list: List, output_filename: str) -> None:
        # todo: write generator
        pass
