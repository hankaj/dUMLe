from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.funtion_object import FunctionObject
from compiler.utils.register import Register
from compiler.utils.output_generator import OutputGenerator


class FunctiondUMLeListener(dUMLeListener):
    def __init__(self, register: Register, output_generator: OutputGenerator):
        self.register = register  # needed for scope management
        self.output_generator = output_generator  # needed to contain function object
        self.current_scope_name = register.global_scope.name  # needed to follow current scope - this information is needed while adding function object to function generator
        self.current_function = None  # reference to current function object - None means that currently the listener is outside the function declaration

    def _exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def _enter_scope(self, ctx):
        self.current_scope_name = ctx.NAME().getText()

    def _enter_diag(self, ctx):
        self._enter_scope(ctx)

    def _exit_diag(self):
        self._exit_scope()

    def _add_enter_ctx_to_fun(self, ctx):
        if self.current_function is not None:
            self.current_function.add_enter_ctx(ctx)

    def _add_exit_ctx_to_fun(self, ctx):
        if self.current_function is not None:
            self.current_function.add_exit_ctx(ctx)

    def enterFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        function_name = ctx.NAME().getText()

        if ctx.arg_list(1):
            argument_names = [name.getText() for name in ctx.arg_list(0).NAME()]
            return_names = [name.getText() for name in ctx.arg_list(1).NAME()]
        else:
            argument_names = []
            return_names = [name.getText() for name in ctx.arg_list(0).NAME()]

        self.current_function = FunctionObject(function_name, argument_names, return_names)
        self._enter_scope(ctx)

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self._exit_scope()
        self.output_generator.add_function(self.current_scope_name, self.current_function.name, self.current_function)
        self.current_function = None

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._enter_diag(ctx)

    def exitSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._exit_diag()

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._enter_diag(ctx)

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._exit_diag()

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._enter_diag(ctx)

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._exit_diag()

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        self._add_enter_ctx_to_fun(ctx)

    def exitClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterActor(self, ctx: dUMLeParser.ActorContext):
        self._add_enter_ctx_to_fun(ctx)

    def exitActor(self, ctx: dUMLeParser.ActorContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        self._add_enter_ctx_to_fun(ctx)

    def exitUse_case(self, ctx: dUMLeParser.Use_caseContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterBlock(self, ctx: dUMLeParser.BlockContext):
        self._add_enter_ctx_to_fun(ctx)

    def exitBlock(self, ctx: dUMLeParser.BlockContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterNote(self, ctx: dUMLeParser.NoteContext):
        self._add_enter_ctx_to_fun(ctx)

    def exitNote(self, ctx: dUMLeParser.NoteContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterConnection(self, ctx: dUMLeParser.ConnectionContext):
        self._add_enter_ctx_to_fun(ctx)

    def exitConnection(self, ctx: dUMLeParser.ConnectionContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterPackage_declaration(self, ctx: dUMLeParser.Package_declarationContext):
        self._add_enter_ctx_to_fun(ctx)

    def exitPackage_declaration(self, ctx: dUMLeParser.Package_declarationContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterTheme(self, ctx: dUMLeParser.ThemeContext):
        self._add_enter_ctx_to_fun(ctx)

    def exitTheme(self, ctx: dUMLeParser.ThemeContext):
        self._add_exit_ctx_to_fun(ctx)

    def enterAssignment(self, ctx: dUMLeParser.AssignmentContext):
        self._add_enter_ctx_to_fun(ctx)

    def exitAssignment(self, ctx: dUMLeParser.AssignmentContext):
        self._add_exit_ctx_to_fun(ctx)
