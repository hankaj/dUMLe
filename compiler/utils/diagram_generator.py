from compiler.utils.output_generator import Mode
from typing import List
from compiler.utils.object import Object



class DiagGenerator:
    def __init__(self):
        self.objects = []

    def generate(self, mode: Mode, object_list_names: List[str] | None = None) -> str:
        # todo: support mode
        if object_list_names is None:
            return self._generate_all()
        else:
            return "".join(obj.generate_all() for obj in self.objects if obj.name in object_list_names)

    def _generate_all(self) -> str:
        return "".join(obj.generate_all() for obj in self.objects)

    def get_object(self, name: str) -> Object:
        for obj in self.objects:
            if obj.name == name:
                return obj
        raise Exception(f"Cannot find object with given name {name}")
