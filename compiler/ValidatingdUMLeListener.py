from compiler.dUMLeListener import dUMLeListener
from compiler.utils.register import Register
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.error_message import ErrorMessage


class ValidatingdUMLeListener(dUMLeListener):

    def __init__(self, register: Register, error: ErrorMessage):
        self.register = register
        self.error = error
        self.current_scope_name = register.global_scope.name
        self.is_in_function = False

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
        self.enter_scope(ctx)

    def enterUse_case_diagram(self, ctx:dUMLeParser.Use_case_diagramContext):
        self.enter_scope(ctx)

    def enterClass_diagram(self, ctx:dUMLeParser.Class_diagramContext):
        self.enter_scope(ctx)

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = False
        self.exit_scope()

    def exitSeq_diagram(self, ctx:dUMLeParser.Seq_diagramContext):
        self.exit_scope()

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self.exit_scope()

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self.exit_scope()

    def enterFun_call(self, ctx: dUMLeParser.Fun_callContext):
        fun_name = ctx.name().getText()
        fun_arg_count = len(ctx.arg_list_include_scope().arg_name())
        fun_descriptor = self.register.get_function_descriptor_in_scope(fun_name, self.current_scope_name)

        if fun_descriptor.n_arguments != fun_arg_count:
            self.error.errors.append(f"Incorrect number of attributes was passed to \"{fun_name}\" function."
                                     f" Expected: {fun_descriptor.n_arguments}. Got: { fun_arg_count}."
                                     f" Line: {ctx.stop.line}")
            return

    def enterAssignment(self, ctx:dUMLeParser.AssignmentContext):
        returns_count = len(ctx.arg_list().NAME())
        if ctx.fun_call() is not None:  # function was called here
            fun_name = ctx.fun_call().name().getText()
            fun_descriptor = self.register.get_function_descriptor_in_scope(fun_name, self.current_scope_name)
            if fun_descriptor.n_returns != returns_count:
                self.error.errors.append(f"Wrong number of returns. Expected: {fun_descriptor.n_returns}. "
                                         f"Got: {returns_count}. Line: {ctx.stop.line}")
                return
        elif ctx.arg_list_include_scope():
            n_values_to_assign = len(ctx.arg_list_include_scope().arg_name())
            if n_values_to_assign != returns_count:
                self.error.errors.append(f"Cannot unpack {n_values_to_assign} objects to {returns_count} objects. "
                                         f"Line: {ctx.stop.line}")
                return
        else:  # list declaration here
            if returns_count > 1:  # incorrect list declaration
                self.error.errors.append(f"Cannot unpack list to {returns_count} objects. Line: {ctx.stop.line}")
                return
