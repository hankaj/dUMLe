from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.object import Theme, Actor, UseCase, Connection, Block, Note, Package
from compiler.utils.register import Register
from compiler.utils.output_generator import OutputGenerator


class ExecutiondUMLeListener(dUMLeListener):
    def __init__(self, register: Register, output_generator: OutputGenerator):
        self.output_generator = output_generator
        self.register = register
        self.current_scope_name = self.register.global_scope.name
        self.is_in_diagram = False
        self.is_in_function = False
        self.current_diagram_name = ""

    def exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def enter_scope(self, ctx):
        self.current_scope_name = ctx.NAME().getText()

    def enterFun_declaration(self, ctx:dUMLeParser.Fun_declarationContext):
        self.is_in_function = True
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
        self.exit_scope()

    def exitSeq_diagram(self, ctx:dUMLeParser.Seq_diagramContext):
        self._exit_diag()

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._exit_diag()

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._exit_diag()

    def enterExecution(self, ctx:dUMLeParser.ExecutionContext):
        if self.is_in_function:
            raise Exception("Cannot execute diagiam inside the function")

        if not self.is_in_diagram and not ctx.NAME(0):
            raise Exception("Diagram name is required in global exectution. Please provide the name of the diagram that you want to execute")

        diag_name = self.current_diagram_name
        file_name = self.current_diagram_name + ".png"
        mode = None
        object_list = None

        if ctx.NAME(0):
            diag_name = ctx.NAME(0).getText()

        if ctx.TEXT():
            file_name = ctx.TEXT().getText()[1:-1]
            if file_name[-4:] != ".png":
                raise Exception("The only supported extension is png. Please provide the png file")

        if ctx.MODE():
            mode = ctx.MODE().getText()

        if ctx.list_declaration():
            object_list = [name.getText() for name in ctx.list_declaration().name()]
        elif ctx.list_access():
            raise Exception("List access is not supported")
        elif ctx.NAME(1):
            raise Exception("List name is not supported")
        elif ctx.obj_access():
            raise Exception("Object access is not supported")

        for diagram_generator in self.output_generator.diagram_generators:
            self.output_generator.generate(diagram_generator, mode, object_list, file_name)
