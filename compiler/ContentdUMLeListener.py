from copy import deepcopy
from enum import Enum, auto
from typing import Tuple, List

from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.exceptions import RecursionDepthException
from compiler.utils.register import Register
from compiler.utils.object import Object, Actor, UseCase, Class, Connection, Block, Note, Package
from compiler.utils.output_generator import OutputGenerator
from compiler.utils.diagram_generator import DiagGenerator, DiagType


class ContentdUMLeListenerMode(Enum):
    NOT_ACTIVE = auto()
    FUNCTION = auto()
    MAIN = auto()


class ContentdUMLeListener(dUMLeListener):
    def __init__(self, register: Register, output_generator: OutputGenerator):
        # needed for both modes
        self.register = register
        self.output_generator = output_generator

        # useful when content listener is called by main.py
        self.current_scope_name = None
        self.is_in_diagram = None
        self.is_in_function = None
        self.current_diagram_type = None
        self.current_function_name = None
        self.current_diagram_name = None

        # useful when content listener is called by user declared function
        self.created_objects = None

        # flag for the mode
        self.mode = ContentdUMLeListenerMode.NOT_ACTIVE

    def _enter_diag(self, ctx, diag_type: DiagType):
        self._enter_scope(ctx)
        self.is_in_diagram = True
        self.current_diagram_name = ctx.NAME().getText()
        self.current_diagram_type = diag_type
        self.output_generator.diagram_generators[self.current_diagram_name] = DiagGenerator(diag_type)

    def _exit_diag(self):
        self.current_diagram_name = ""
        self.current_diagram_type = None
        self.is_in_diagram = False
        self._exit_scope()

    def _enter_scope(self, ctx):
        self.current_scope_name = ctx.NAME().getText()

    def _exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def _get_scope_if_exists(self, name: str) -> Tuple[str | None, str]:
        if "&" in name:
            return name.split("&")[0], name.split("&")[1]
        return None, name

    def _add_object(self, object: Object):
        if self.mode is ContentdUMLeListenerMode.MAIN:
            if self.is_in_diagram:
                self.output_generator.diagram_generators[self.current_diagram_name].objects.append(object)
            elif not self.is_in_function:  # global
                self.output_generator.global_objects[object.name] = object
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            self.created_objects.append(object)
        else:
            raise Exception("Content listener is not activated. Specify the source of the code")

    def set_global_listener(self):
        if self.mode != ContentdUMLeListenerMode.NOT_ACTIVE:
            raise Exception("Cannot activate content listener. Content listener is already activated")

        # activating content listener to main mode
        self.current_scope_name = self.register.global_scope.name
        self.is_in_diagram = False
        self.is_in_function = False
        self.current_diagram_type = None
        self.current_function_name = ""
        self.current_diagram_name = ""
        self.mode = ContentdUMLeListenerMode.MAIN

    def set_function_listener(self, parameters: List['Object'], scope_name: str, function_name: str):
        if self.mode != ContentdUMLeListenerMode.NOT_ACTIVE:
            raise Exception("Cannot activate content listener. Content listener is already activated")

        # activating content listener to function mode
        self.created_objects = parameters
        self.current_scope_name = scope_name
        self.current_function_name = function_name
        self.mode = ContentdUMLeListenerMode.FUNCTION

    def enterFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self._enter_scope(ctx)
        self.is_in_function = True
        self.current_function_name = ctx.NAME().getText()

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = False
        self.current_function_name = ""
        self._exit_scope()

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._enter_diag(ctx, DiagType.CLASS)

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._exit_diag()

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._enter_diag(ctx, DiagType.USE_CASE)

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._exit_diag()

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._enter_diag(ctx, DiagType.SEQUENCE)

    def exitSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._exit_diag()

    def enterActor(self, ctx: dUMLeParser.ActorContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.USE_CASE:
            raise Exception(f"You cannot define actor in {self.current_diagram_type}. Line: {ctx.stop.line}")
        actor = Actor(ctx)
        self._add_object(actor)

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.USE_CASE:
            raise Exception(f"You cannot define use case in {self.current_diagram_type}. Line: {ctx.stop.line}")
        use_case = UseCase(ctx)
        self._add_object(use_case)

    def enterBlock(self, ctx: dUMLeParser.BlockContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.SEQUENCE:
            raise Exception(f"You cannot define block in {self.current_diagram_type}. Line: {ctx.stop.line}")
        block = Block(ctx)
        self._add_object(block)

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.CLASS:
            raise Exception(f"You cannot define class in {self.current_diagram_type}. Line: {ctx.stop.line}")
        class_object = Class(ctx)
        self._add_object(class_object)

    def enterNote(self, ctx: dUMLeParser.NoteContext):
        note = Note(ctx)

        if self.mode is ContentdUMLeListenerMode.MAIN:
            if self.is_in_diagram:
                for object in self.output_generator.diagram_generators[self.current_diagram_name].objects:
                    if object.name == note.object_name:
                        object.add_note(note)
                        break
            elif not self.is_in_function:  # global
                self.output_generator.global_objects[note.object_name].add_note(note)
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            for object in self.created_objects:
                if object.name == note.object_name:
                    object.add_note(note)
                    break

    def enterConnection(self, ctx: dUMLeParser.ConnectionContext):
        connection = Connection(ctx)
        # todo: below should be checked in validating/indexing listener
        # if not self.register.is_object_in_scope(connection.source_object_name, self.current_scope_name):
        #     raise Exception(f"No {connection.source_object_name} object in {self.current_scope_name} scope")
        # if not self.register.is_object_in_scope(connection.destination_object_name, self.current_scope_name):
        #     raise Exception(f"No {connection.destination_object_name} object in {self.current_scope_name} scope")

        if self.mode is ContentdUMLeListenerMode.MAIN:
            if self.is_in_diagram:
                for object in self.output_generator.diagram_generators[self.current_diagram_name].objects:
                    if object.name == connection.source_object_name:
                        object.add_connection(connection)
                        break
                if self.current_diagram_type == DiagType.SEQUENCE:  # todo: dont like this idea - problematic for function call
                    self.output_generator.diagram_generators[self.current_diagram_name].sequences.append(connection)
            elif not self.is_in_function:  # global
                self.output_generator.global_objects[connection.source_object_name].add_connection(connection)
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            for object in self.created_objects:
                if object.name == connection.source_object_name:
                    object.add_connection(connection)
                    break

    def enterPackage_declaration(self, ctx: dUMLeParser.Package_declarationContext):
        return
        # todo: adjust package
        # TODO: support object access and list access
        # if self.is_in_function:
        #     raise Exception(f"Cannot declare package inside of the function")
        # object_names = [name.getText() for name in ctx.NAME()]
        # object_names.pop(0)
        # is_deep_copy = [True for _ in enumerate(object_names)]
        # try:
        #     objects = self.output_generator.get_objects(object_names, is_deep_copy, self.current_scope_name)
        # except ObjectNotDeclaredException as e:
        #     raise Exception(f"{e} Line: {ctx.stop.line}")
        # try:
        #     package = Package(ctx, objects)
        # except WrongDiagramTypeException as e:
        #     raise Exception(f"{e} Line {ctx.stop.line}")
        # if self.is_in_diagram:
        #     self.output_generator.diagram_generators[self.current_diagram_name].objects.append(package)
        #     for o in package.objects:
        #         objects = self.output_generator.diagram_generators[self.current_diagram_name].objects
        #         for existing_object in objects:
        #             if existing_object.name == o.name:
        #                 objects.remove(existing_object)
        #                 break
        # else:
        #     self.output_generator.global_objects[package.name] = package

    def enterTheme(self, ctx: dUMLeParser.ThemeContext):
        raise Exception(f"Theme is not yet supported. Line: {ctx.stop.line}")

    def _get_arg_copy_from_diagram(self, arg_names: List[str], is_deep_copy: List[bool]):
        # get copy of the objects from diagram generator
        arg_list = self.output_generator.get_objects(arg_names, is_deep_copy, self.current_scope_name)

        return arg_list

    def _get_arg_copy_from_function(self, arg_names: List[str], is_deep_copy: List[bool]):
        arg_list = []
        for object_name, is_deep_copy in zip(arg_names, is_deep_copy):
            # find the object
            found_object = None
            for function_object in self.created_objects:
                if function_object.name == object_name:
                    found_object = function_object
                    break

            # check if the object was found  # todo: move to validating/indexing in the final version
            if found_object is None:
                raise Exception("Object was not declared in this scope")

            # copy found object and add it to arg_list
            copied_object = deepcopy(found_object)
            if not is_deep_copy:
                copied_object.connections = {}
            arg_list.append(copied_object)

        return arg_list

    def _call_function(self, fun_ctx, returned_arg_names: List[str], line):
        # read arg names and mark if perform a deep copy
        arg_names = [arg_name.name().getText() for arg_name in fun_ctx.arg_list_include_scope().arg_name()]
        is_deep_copy = [True if arg_name.DEEP_COPY() else False for arg_name in
                        fun_ctx.arg_list_include_scope().arg_name()]

        # get current scope and function name
        scope_name, fun_name = self._get_scope_if_exists(fun_ctx.name().getText())
        if scope_name is None:
            scope_name = self.register.get_nearest_scope_name(self.current_scope_name, fun_name)

        # copy argument objects from proper place
        if self.mode is ContentdUMLeListenerMode.MAIN:
            # get copy of the objects from diagram generator
            arg_list = self._get_arg_copy_from_diagram(arg_names, is_deep_copy)
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            # get copy of the objects from the list of objects created by the function
            arg_list = self._get_arg_copy_from_function(arg_names, is_deep_copy)
        else:  # wrong mode
            raise Exception("Wrong mode. Cannot call the function")

        # call the function and set up maximum recursion depth
        function = self.output_generator.get_function(scope_name, fun_name)
        function.max_recursion_depth_count = 1  # default max depth
        if fun_ctx.NUMBER():
            function.max_recursion_depth_count = int(fun_ctx.NUMBER().getText())
        function.activate()  # this will increase the current recursion depth and throw the RecursionDepthException if the limit is reached
        returned_objects = function.call(self.output_generator, self.register, arg_list, returned_arg_names, self.current_scope_name)
        function.release()  # this will decrease the current recursion depth

        # verify if the object is legal for the current diagram
        if self.is_in_diagram:
            allowed_types = self.output_generator.diagram_generators[self.current_diagram_name].available_object_types
            for returned_object in returned_objects:
                if type(returned_object) not in allowed_types:
                    raise Exception(f"You cannot create {type(returned_object)} object in {self.current_diagram_type}")

        # return the result
        return returned_objects

    def enterAssignment(self, ctx: dUMLeParser.AssignmentContext):
        returned_arg_names = [name.getText() for name in ctx.arg_list().NAME()]
        returned_objects = []

        # execute proper assignment
        if ctx.list_declaration():  # list declaration (a = [])
            raise Exception(f"List declaration not supported. Line: {ctx.stop.line}")
        elif ctx.fun_call():  # function call (a = fun())
            try:
                if self.mode is ContentdUMLeListenerMode.MAIN and self.is_in_function:  # ignore calling function in other functions
                    return
                returned_objects = self._call_function(ctx.fun_call(), returned_arg_names, ctx.stop.line)
            except RecursionDepthException:
                return  # just leave the function if the max depth of the recursion was reached
        elif ctx.arg_list_include_scope():  # simple assignment (x, y, z = a, b, c)
            arg_names = [arg_name.name().getText() for arg_name in ctx.arg_list_include_scope().arg_name()]
            is_deep_copy = [True if arg_name.DEEP_COPY() else False for arg_name in
                            ctx.arg_list_include_scope().arg_name()]

            if self.mode is ContentdUMLeListenerMode.MAIN:
                arg_list = self._get_arg_copy_from_diagram(arg_names, is_deep_copy)
            elif self.mode is ContentdUMLeListenerMode.FUNCTION:
                arg_list = self._get_arg_copy_from_function(arg_names, is_deep_copy)
            else:  # wrong mode
                raise Exception("Wrong mode. Cannot call the function")

            returned_objects = Object.change_names(arg_list, returned_arg_names)

        # add returned object to proper scope
        if self.mode is ContentdUMLeListenerMode.MAIN:
            for object in returned_objects:
                if self.is_in_diagram:
                    if object.is_package and object.type != self.current_diagram_type:
                        raise Exception(f"You cannot add package of type {object.type} to {self.current_diagram_type}")
                    objects = self.output_generator.diagram_generators[self.current_diagram_name].objects
                    for existing_object in objects:
                        if existing_object.name == object.name:
                            objects.remove(existing_object)
                            break
                    objects.append(object)
                elif not self.is_in_function:  # global
                    objects = self.output_generator.global_objects
                    for existing_object in objects:
                        if existing_object.name == object.name:
                            objects.remove(existing_object)
                            break
                    self.output_generator.global_objects[object.name] = object
        elif self.mode is ContentdUMLeListenerMode.FUNCTION:
            for object in returned_objects:
                if object.is_package:
                    raise Exception(f"You cannot add package to function. Line: {ctx.stop.line}")
                for existing_object in self.created_objects:
                    if existing_object.name == object.name:
                        self.created_objects.remove(existing_object)
                        break
                self.created_objects.append(object)
        else:  # wrong mode
            raise Exception("Wrong mode. Cannot call the function")
