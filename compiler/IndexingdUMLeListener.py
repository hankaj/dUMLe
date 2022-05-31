from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.register import Register, Scope, FunctionDescriptor
from compiler.utils.error_message import ErrorMessage


class IndexingdUMLeListener(dUMLeListener):
    def __init__(self, register: Register, error: ErrorMessage):
        self.register = register
        self.error = error
        self.current_scope_name = register.global_scope.name
        self.is_in_function = False
        self.nested_function_counter = 0

    def register_diagram_creation(self, ctx):
        if self.is_in_function:
            self.error.errors.append(f"Cannot create diagram inside the function. Line: {ctx.stop.line}")
            return

        diag_name = ctx.NAME().getText()
        self.register.add_object_to_scope(diag_name, self.current_scope_name)
        diag_scope = Scope(diag_name, self.current_scope_name, [], {})
        self.register.scopes[diag_name] = diag_scope
        self.current_scope_name = diag_name

    def exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def enterFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.nested_function_counter += 1
        if self.is_in_function:
            self.error.errors.append(f"Functions cannot be nested. Line: {ctx.stop.line}")
            return

        self.is_in_function = True
        fun_name = ctx.NAME().getText()

        if ctx.arg_list(1) is None:
            n_arguments = 0
            n_returns = len(ctx.arg_list(0).NAME())
        else:
            n_arguments = len(ctx.arg_list(0).NAME())
            n_returns = len(ctx.arg_list(1).NAME())

        function_descriptor = FunctionDescriptor(n_arguments, n_returns)
        fun_scope = Scope(fun_name, self.current_scope_name, [], {})

        self.register.add_function_to_scope(fun_name, function_descriptor, self.current_scope_name)
        self.register.scopes[fun_name] = fun_scope
        self.current_scope_name = fun_name

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self.register_diagram_creation(ctx)

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self.register_diagram_creation(ctx)

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self.register_diagram_creation(ctx)

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.nested_function_counter -= 1
        if self.nested_function_counter == 0:
            self.is_in_function = False
            self.exit_scope()

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self.exit_scope()

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self.exit_scope()

    def exitSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self.exit_scope()

    def enterActor(self, ctx: dUMLeParser.ActorContext):
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def enterBlock(self, ctx: dUMLeParser.BlockContext):
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def enterNote(self, ctx: dUMLeParser.NoteContext):
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def enterTheme(self, ctx: dUMLeParser.ThemeContext):
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def enterPackage_declaration(self, ctx: dUMLeParser.Package_declarationContext):
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)
