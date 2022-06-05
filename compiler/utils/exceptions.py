class ObjectNotDeclaredException(BaseException):
    def __init__(self, object_name: str):
        self.object_name = object_name

    def __str__(self):
        return f"Object {self.object_name} not found"


class WrongDiagramTypeException(BaseException):
    def __init__(self,  diag_type, obj_type):
        self.diag_type = diag_type
        self.obj_type = obj_type

    def __str__(self):
        return f"Cannot add {self.obj_type} to {self.diag_type}"
