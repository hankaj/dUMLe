from abc import ABC, abstractmethod
from compiler.utils.output_generator import Mode
from typing import List

# class DiagramGenerator(ABC):
#
#     @abstractmethod
#     def generate(self, mode: Mode, object_list: List):
#         pass


class DiagGenerator:
    def __init__(self):
        self.objects = []

    def generate(self, mode: Mode, object_list_names: List[str] | None = None) -> str:
        # todo: support mode
        if object_list_names is None:
            return self._generate_all()
        else:
            return "".join(obj.generate() for obj in self.objects if obj.name in object_list_names)

    def _generate_all(self) -> str:
        return "".join(obj.generate() for obj in self.objects)
