from compiler.utils.output_generator import Mode
from typing import List, Optional
from compiler.utils.object import Object, Class, UseCase, Actor, Block
from enum import Enum, auto
from compiler.utils.exceptions import ObjectNotDeclaredException


class DiagType(Enum):
    CLASS = auto()
    USE_CASE = auto()
    SEQUENCE = auto()


OBJECTS_IN_DIAGRAMS = {DiagType.CLASS: [Class], DiagType.USE_CASE: [UseCase, Actor], DiagType.SEQUENCE: [Block]}


class DiagGenerator:
    def __init__(self, diag_type: DiagType):
        self.type = diag_type
        self.available_object_types = OBJECTS_IN_DIAGRAMS[diag_type]
        self.objects = []

    def generate(self, mode: Mode, object_list_names: Optional[List[str]] = None) -> str:
        # todo: support mode

        if object_list_names is None:
            return self._generate_all()
        else:
            return "".join(obj.generate() for obj in self.objects if obj.name in object_list_names) \
                + "".join(obj.generate_connections(object_list_names) for obj in self.objects if obj.name in object_list_names)

    def _generate_all(self) -> str:
        return "".join(obj.generate() for obj in self.objects)+"".join(obj.generate_connections() for obj in self.objects)

    def get_object(self, name: str) -> Object:
        for obj in self.objects:
            if obj.name == name:
                return obj
        raise ObjectNotDeclaredException(name)
