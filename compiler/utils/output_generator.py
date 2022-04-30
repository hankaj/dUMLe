from enum import Enum, auto
from typing import List
from plantuml import PlantUML
from compiler.utils.function_generator import FunctionGenerator
import os


class Mode(Enum):
    """
    dosc for Mode
    """
    ALL = auto()
    BRIEF = auto()


class OutputGenerator:
    """ docs for OutputGenerator"""

    def __init__(self):
        self.server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        self.global_objects = {}
        self.diagram_generators = {}
        self._functions = {}

    def generate(self, diag_name: str, mode: Mode, object_list: List, output_filename: str = None) -> None:
        diagram_generator = self.diagram_generators[diag_name]
        output = "@startuml\n"
        output += diagram_generator.generate(mode, object_list)
        output += "@enduml"
        with open("results/output.txt", 'w+') as fp:
            fp.write(output)
        if output_filename is None:
            output_filename = diag_name + "_".join(obj_name for obj_name in object_list)
        self.server.processes_file(filename="results/output.txt", outfile=output_filename)
        os.remove("results/output.txt")

    def add_function(self, scope_name: str, function_name: str, function_generator: FunctionGenerator) -> None:
        self._functions[scope_name + ":" + function_name] = function_generator

    def get_function(self, scope_name: str, function_name: str) -> FunctionGenerator:
        return self._functions[scope_name + ":" + function_name]
