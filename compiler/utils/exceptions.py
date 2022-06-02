class ObjectNotDeclaredException(BaseException):
    def __init__(self, object_name):
        self.object_name = object_name

    def __str__(self):
        return f"Object {self.object_name} not found"
