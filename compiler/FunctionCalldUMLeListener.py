from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.register import Register
from compiler.utils.output_generator import OutputGenerator


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
        self.enter_scope(ctx)

    def enterSeq_diagram(self, ctx:dUMLeParser.Seq_diagramContext):
        self.is_in_diagram = True
        self.enter_scope(ctx)

    def enterUse_case_diagram(self, ctx:dUMLeParser.Use_case_diagramContext):
        self.is_in_diagram = True
        self.enter_scope(ctx)

    def enterClass_diagram(self, ctx:dUMLeParser.Class_diagramContext):
        self.is_in_diagram = True
        self.enter_scope(ctx)

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = False
        self.exit_scope()

    def exitSeq_diagram(self, ctx:dUMLeParser.Seq_diagramContext):
        self.is_in_diagram = False
        self.exit_scope()

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self.is_in_diagram = False
        self.exit_scope()

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self.is_in_diagram = False
        self.exit_scope()

    def enterNamed_list_declaration(self, ctx:dUMLeParser.Named_list_declarationContext):
        if ctx.fun_call():
            args = []
            #  for arg_names in ctx.
            if self.is_in_function:
                self.output_generator.get_function(self.register.parent_name(self.current_function_name),
                                                    self.current_function_name).add_note(note)
            elif self.is_in_diagram:
                for object in self.output_generator.diagram_generators[self.current_diagram_name]:
                    if object.name == note.object_name:
                        object.add_note(note)
                        break
            else:  # global
                self.output_generator.global_objects[note.object_name].add_note(note)
        else:  # list declaration
            raise Exception("List declaration not supported")
            pass