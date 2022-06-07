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
        self.current_function = FunctionObject(function_name, [name.GetText() for name in ctx.arg_list()])

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.output_generator.add_function(self.current_scope_name, self.current_function.name, self.current_function)
        self.current_function = None
        self._exit_scope()

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
