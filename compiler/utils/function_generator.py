from compiler.utils.register import FunctionDescriptor
from compiler.utils.object import Object, Connection, Note
from copy import deepcopy, copy
from typing import List
from compiler.dUMLeParser import dUMLeParser


class FunctionGenerator:
    def __init__(self, function_descriptor: FunctionDescriptor):
        self.n_arguments = function_descriptor.n_arguments
        self.n_returns = function_descriptor.n_returns
        self.fixed_objects = []
        self.modifiable_args = []
        self.modifiable_arg_names = []
        self.return_object_names = []
        self.code_executed_in_call = {"activation": [], "connection": [], "note": []}

    def _process(self, args: List[Object]) -> None:
        for i, arg in enumerate(args):
            arg_copy = copy(arg)
            arg_copy.name = self.modifiable_arg_names[i]
            self.modifiable_args.append(arg_copy)

    def _execute_activation_ctx(self, ctx: dUMLeParser.Block_operationContext):
        # todo: write activation
        pass

    def add_connection(self, connection: Connection) -> None:
        self.code_executed_in_call["connection"].append(connection)

    def add_note(self, note: Note) -> None:
        self.code_executed_in_call["note"].append(note)

    def call(self, args) -> List[Object]:
        self._process(args)

        result = []
        for result_object_name in self.return_object_names:
            for fixed_object in self.fixed_objects:
                if fixed_object.name == result_object_name:
                    result.append(copy(fixed_object))
            for modifiable_arg in self.modifiable_args:
                if modifiable_arg.name == result_object_name:
                    result.append(copy(modifiable_arg))

        self.modifiable_args.clear()

        # for operation, objects in self.code_executed_in_call:
        #     if operation == "activation":
        #         for ctx in objects:
        #             self._execute_activation_ctx(ctx)
        #     elif operation == "connection":
        #         for connection in objects:
        #             connection.source_object_name

        return result
