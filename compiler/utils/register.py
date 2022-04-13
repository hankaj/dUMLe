from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class Scope:
    name: str
    parent: Optional[str]
    object_register: List[str]
    function_register: Dict[str, str]    # tu będzie nazwa funkcji: jej treść


class Register:
    def __init__(self):
        self.global_scope = Scope(parent=None, object_register=[], function_register={}, name='global')
        self.scopes = {'global': self.global_scope}

    def is_object_in_scope(self, object_name: str, scope_name: str) -> bool:
        if scope_name is None:
            return False
        if object_name not in self.scopes[scope_name].object_register:
            return self.is_object_in_scope(object_name, self.scopes[scope_name].parent_name)
        return True

    def is_function_in_scope(self, function_name: str, scope_name: str) -> bool:
        if scope_name is None:
            return False
        if function_name not in self.scopes[scope_name].function_register.keys():
            return self.is_function_in_scope(function_name, self.scopes[scope_name].parent_name)
        return True

    def add_object_to_scope(self, object_name: str, scope_name: str) -> None:
        if self.is_object_in_scope(object_name, scope_name):
            raise Exception("This object is already declared")
        self.scopes[scope_name].object_register.append(object_name)
    
    def add_function_to_scope(self, function_name: str, function_body: str, scope_name: str) -> None:
        if self.is_function_in_scope(function_name, scope_name):
            raise Exception("This function is already declared")
        self.scopes[scope_name].function_register[function_name] = function_body
        