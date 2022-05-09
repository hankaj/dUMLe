from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.register import Register
from compiler.utils.output_generator import OutputGenerator
from typing import List, Tuple
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

    def _change_names(self, objects: List[Object], names: List[str]) -> List[Object]:
        new_names = {object.name: new_name for object, new_name in zip(objects, names)}
        print(new_names)
        for object in objects:
            new_connections = {}
            for destination_object_name, connections in object.connections.items():
                for connection in connections:
                    connection.source_object_name = new_names[connection.source_object_name]
                    connection.destination_object_name = new_names[connection.destination_object_name]
                    if connection.destination_object_name not in new_connections:
                        new_connections[connection.destination_object_name] = [connection]
                    else:
                        new_connections[connection.destination_object_name].append(connection)
            object.name = new_names[object.name]

        return objects

    def _get_scope_if_exists(self, name: str) -> Tuple[str|None, str]:
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

    def enterNamed_list_declaration(self, ctx: dUMLeParser.Named_list_declarationContext):
        if ctx.fun_call():
            fun_ctx = ctx.fun_call()
            scope_name, fun_name = self._get_scope_if_exists(fun_ctx.name().getText())
            if scope_name is None:
                scope_name = self.register.get_nearest_scope_name(self.current_scope_name, fun_name)

            returned_arg_names = [name.getText() for name in ctx.arg_list().NAME()]
            arg_names = [name.getText() for name in fun_ctx.arg_list_include_scope().name()]
            arg_list = self.output_generator.get_objects(arg_names, self.current_scope_name)

            returned_objects = self.output_generator.get_function(scope_name, fun_name).call(arg_list)
            returned_objects = self._change_names(returned_objects, returned_arg_names)

            for object in returned_objects:
                if self.is_in_function:
                    self.output_generator.get_function(self.register.get_nearest_scope_name(self.current_scope_name, self.current_function_name),
                                                        self.current_function_name).fixed_objects.append(object)
                elif self.is_in_diagram:
                    self.output_generator.diagram_generators[self.current_diagram_name].objects.append(object)
                else:  # global
                    self.output_generator.global_objects.append(object)
        else:  # list declaration
            raise Exception("List declaration not supported")
            pass