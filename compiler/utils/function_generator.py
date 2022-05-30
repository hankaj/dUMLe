from compiler.utils.register import FunctionDescriptor
from compiler.utils.object import Object, Connection, Note
from copy import deepcopy, copy
from typing import List, Tuple
from compiler.dUMLeParser import dUMLeParser


class FunctionGenerator:
    def __init__(self, function_descriptor: FunctionDescriptor):
        self.n_arguments = function_descriptor.n_arguments
        self.n_returns = function_descriptor.n_returns
        self.fixed_objects = []
        self.modifiable_args = []
        self.modifiable_arg_names = []
        self.return_object_names = []

        self.connections_to_create = []
        self.activations_to_create = []
        self.notes_to_create = []

    def _process(self, args: List[Object]) -> None:
        # todo: delete or reuse
        # for i, arg in enumerate(args):
            # arg_copy = copy(arg)
            # arg_copy.name = self.modifiable_arg_names[i]
            # self.modifiable_args.append(arg_copy)
        #self.modifiable_args = [copy(arg) for arg in args]
        self.modifiable_args = Object.change_names(args, self.modifiable_arg_names)

    def call(self, args: List[Object]) -> List[Object]:
        self.modifiable_args = Object.change_names(args, self.modifiable_arg_names)

        result = []
        for result_object_name in self.return_object_names:
            for fixed_object in self.fixed_objects:
                if fixed_object.name == result_object_name:
                    result.append(copy(fixed_object))
            for modifiable_arg in self.modifiable_args:
                if modifiable_arg.name == result_object_name:
                    result.append(copy(modifiable_arg))

        for connection in self.connections_to_create:
            for object in result:
                if object.name == connection.source_object_name:
                    object.add_connection(deepcopy(connection))

        for note in self.notes_to_create:
            for object in result:
                if object.name == note.object_name:
                    object.add_note(note)

        # todo: support activations

        self.modifiable_args.clear()

        return result
