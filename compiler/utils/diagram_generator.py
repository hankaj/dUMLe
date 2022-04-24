from abc import ABC, abstractmethod
from compiler.utils.output_generator import Mode
from typing import List

class DiagramGenerator(ABC):

    @abstractmethod
    def generate(self, mode: Mode, object_list: List):
        pass


class DiagClassGenerator(DiagramGenerator):
    def __init__(self):
        self.objects = {}

    def generate(self, mode: Mode, object_list: List[str] | None = None):
        output = ""
        if object_list is None:
            self._generate_all()
        for obj_name in object_list:
            output += self.objects[obj_name].generate()

    def _generate_all(self):
        output = ""
        for obj_name, obj in self.objects.items():
            output += obj.generate()