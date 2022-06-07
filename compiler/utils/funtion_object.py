from enum import Enum, auto
from typing import List

from antlr4 import ParseTreeWalker

from compiler.utils.object import Object


class RuleType(Enum):
    ENTER = auto()
    EXIT = auto()


class FunctionObject:
    def __init__(self, name: str, argument_names: List[str], return_names: List[str]):
        self.name = name  # the name of the function
        self.ctx = []  # the list that contains ctx objects that have to be called sequentially
        self.argument_names = argument_names
        self.return_names = return_names

    def call(self, output_generator, register, parameters: List[Object], returned_object_names: List[str], scope_name: str) -> List:
        # changing name of the parameters
        parameters = Object.change_names(parameters, self.argument_names)

        # creating walker for the function
        walker = ParseTreeWalker()

        # creating new listener for the function
        from compiler.ContentdUMLeListener import ContentdUMLeListener
        listener = ContentdUMLeListener(register, output_generator)
        listener.set_function_listener(parameters, scope_name, self.name)

        # executing function code
        for single_ctx_tuple in self.ctx:
            if single_ctx_tuple[0] == RuleType.ENTER:
                walker.enterRule(listener, single_ctx_tuple[1])
            elif single_ctx_tuple[0] == RuleType.EXIT:
                walker.exitRule(listener, single_ctx_tuple[1])

        # renaming result and returning proper objects
        returned_objects = []
        for returned_object in listener.created_objects:
            if returned_object.name in self.return_names:
                returned_objects.append(returned_object)

        return Object.change_names(returned_objects, returned_object_names)

    def add_enter_ctx(self, enter_rule):
        self.ctx.append((RuleType.ENTER, enter_rule))

    def add_exit_ctx(self, exit_rule):
        self.ctx.append((RuleType.EXIT, exit_rule))
