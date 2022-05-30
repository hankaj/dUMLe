from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.register import Register
from compiler.utils.output_generator import OutputGenerator
from typing import Tuple
from compiler.utils.object import Object, Connection


class FunctionCalldUMLeListener(dUMLeListener):
    def __init__(self, register: Register, output_generator: OutputGenerator):
        self.register = register
        self.output_generator = output_generator

        self.current_scope_name = register.global_scope.name
        self.is_in_diagram = False
        self.is_in_function = False
        self.current_function_name = ""
        self.current_diagram_name = ""

    def exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def enter_scope(self, ctx):
        self.current_scope_name = ctx.NAME().getText()

    def enterFun_declaration(self, ctx:dUMLeParser.Fun_declarationContext):
        if self.is_in_function:
            return
        self.is_in_function = True
        self.current_function_name = ctx.NAME().getText()
        self.enter_scope(ctx)

    def _enter_diag(self, ctx):
        self.is_in_diagram = True
        self.current_diagram_name = ctx.NAME().getText()
        self.enter_scope(ctx)

    def _exit_diag(self):
        self.current_diagram_name = ""
        self.is_in_diagram = False
        self.exit_scope()

    def enterSeq_diagram(self, ctx:dUMLeParser.Seq_diagramContext):
        self._enter_diag(ctx)

    def enterUse_case_diagram(self, ctx:dUMLeParser.Use_case_diagramContext):
        self._enter_diag(ctx)

    def enterClass_diagram(self, ctx:dUMLeParser.Class_diagramContext):
        self._enter_diag(ctx)

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = False
        self.current_function_name = ""
        self.exit_scope()

    def exitSeq_diagram(self, ctx:dUMLeParser.Seq_diagramContext):
        self._exit_diag()

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._exit_diag()

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._exit_diag()

    def _get_scope_if_exists(self, name: str) -> Tuple['str|None', str]:
        if "&" in name:
            return name.split("&")[0], name.split("&")[1]
        return None, name

    def enterConnection(self, ctx: dUMLeParser.ConnectionContext):
        if self.is_in_function:
            return
        connection = Connection(ctx)
        if self.is_in_diagram:
            for object in self.output_generator.diagram_generators[self.current_diagram_name].objects:
                if object.name == connection.source_object_name:
                    object.add_connection(connection)
                    break
        else: # global
            self.output_generator.global_objects[connection.source_object_name].add_connection(connection)

    def enterAssignment(self, ctx:dUMLeParser.AssignmentContext):
        if ctx.list_declaration():  # list declaration
            raise Exception("List declaration not supported")
            pass

        returned_arg_names = [name.getText() for name in ctx.arg_list().NAME()]
        returned_objects = []

        if ctx.fun_call():
            fun_ctx = ctx.fun_call()
            scope_name, fun_name = self._get_scope_if_exists(fun_ctx.name().getText())
            if scope_name is None:
                scope_name = self.register.get_nearest_scope_name(self.current_scope_name, fun_name)

            arg_names = [arg_name.name().getText() for arg_name in fun_ctx.arg_list_include_scope().arg_name()]
            is_deep_copy = [True if arg_name.DEEP_COPY() else False for arg_name in fun_ctx.arg_list_include_scope().arg_name()]
            arg_list = self.output_generator.get_objects(arg_names, is_deep_copy, self.current_scope_name)

            returned_objects = self.output_generator.get_function(scope_name, fun_name).call(arg_list)
            returned_objects = Object.change_names(returned_objects, returned_arg_names)

        elif ctx.arg_list_include_scope():
            arg_names = [arg_name.name().getText() for arg_name in ctx.arg_list_include_scope().arg_name()]
            is_deep_copy = [True if arg_name.DEEP_COPY() else False for arg_name in ctx.arg_list_include_scope().arg_name()]
            arg_list = self.output_generator.get_objects(arg_names, is_deep_copy, self.current_scope_name)
            returned_objects = Object.change_names(arg_list, returned_arg_names)

        for object in returned_objects:
            if self.is_in_function:
                objects = self.output_generator.get_function(
                    self.register.get_nearest_scope_name(self.current_scope_name, self.current_function_name),
                    self.current_function_name).fixed_objects
                for existing_object in objects:
                    if existing_object.name == object.name:
                        objects.remove(existing_object)
                        break
                objects.append(object)
            elif self.is_in_diagram:
                objects = self.output_generator.diagram_generators[self.current_diagram_name].objects
                for existing_object in objects:
                    if existing_object.name == object.name:
                        objects.remove(existing_object)
                        break
                objects.append(object)
            else:  # global
                objects = self.output_generator.global_objects
                for existing_object in objects:
                    if existing_object.name == object.name:
                        objects.remove(existing_object)
                        break
                objects.append(object)
