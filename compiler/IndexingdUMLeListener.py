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
        self.function_descriptors_to_verify = {}  # dict: fun_name -> List[(fun_descriptor, line_number)] of function descriptors to verify
        self.current_function = None  # reference to current function object - None means that currently the listener is outside the function declaration

    def _register_diagram_creation(self, ctx):
        if self.is_in_function:
            self.error.errors.append(f"Cannot create diagram inside the function. Line: {ctx.stop.line}")
            return

        diag_name = ctx.NAME().getText()
        self.register.add_object_to_scope(diag_name, self.current_scope_name)
        diag_scope = Scope(diag_name, self.current_scope_name, [], {})
        self.register.scopes[diag_name] = diag_scope
        self._enter_scope(ctx)

    def _enter_scope(self, ctx):
        self.current_scope_name = ctx.NAME().getText()

    def _exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._register_diagram_creation(ctx)

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._exit_scope()

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._register_diagram_creation(ctx)

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._exit_scope()

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._register_diagram_creation(ctx)

    def exitSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._exit_scope()

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
        # verify calls of the function that appeared before its declaration
        if fun_name in self.function_descriptors_to_verify.keys():
            for function_tuple in self.function_descriptors_to_verify[fun_name]:
                function_descriptor_to_verify = function_tuple[0]
                line = function_tuple[1]
                if function_descriptor.n_returns != function_descriptor_to_verify.n_returns:
                    self.error.errors.append(f"Wrong number of returns. Expected: {function_descriptor.n_returns}. "
                                             f"Got: {function_descriptor_to_verify.n_returns}. Line: {line}")
                if function_descriptor.n_arguments != function_descriptor_to_verify.n_arguments:
                    self.error.errors.append(f"Incorrect number of attributes was passed to \"{fun_name}\" function."
                                             f" Expected: {function_descriptor.n_arguments}. Got: {function_descriptor_to_verify.n_arguments}."
                                             f" Line: {line}")
            self.function_descriptors_to_verify.pop(fun_name)
        fun_scope = Scope(fun_name, self.current_scope_name, [], {})

        self.register.add_function_to_scope(fun_name, function_descriptor, self.current_scope_name)
        self.register.scopes[fun_name] = fun_scope
        self.current_scope_name = fun_name

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.nested_function_counter -= 1
        if self.nested_function_counter == 0:
            self.is_in_function = False
            self._exit_scope()

    def enterAssignment(self, ctx: dUMLeParser.AssignmentContext):
        for name in ctx.arg_list().NAME():
            self.register.add_object_to_scope(name.getText(), self.current_scope_name)

        ret_arg_count = len(ctx.arg_list().NAME())
        if ctx.fun_call():  # function was called here
            fun_name = ctx.fun_call().name().getText()
            fun_arg_count = len(ctx.fun_call().arg_list_include_scope().arg_name())
            fun_descriptor = self.register.get_function_descriptor_in_scope(fun_name, self.current_scope_name)
            if fun_descriptor is None:  # function was not declared yet
                fun_descriptor = FunctionDescriptor(fun_arg_count, ret_arg_count)
                if fun_name not in self.function_descriptors_to_verify.keys():
                    self.function_descriptors_to_verify[fun_name] = [(fun_descriptor, ctx.stop.line)]
                else:
                    self.function_descriptors_to_verify[fun_name].append((fun_descriptor, ctx.stop.line))
            else:  # function was already declared
                if fun_descriptor.n_returns != ret_arg_count:
                    self.error.errors.append(f"Wrong number of returns. Expected: {fun_descriptor.n_returns}. "
                                             f"Got: {ret_arg_count}. Line: {ctx.stop.line}")
                if fun_descriptor.n_arguments != fun_arg_count:
                    self.error.errors.append(f"Incorrect number of attributes was passed to \"{fun_name}\" function."
                                             f" Expected: {fun_descriptor.n_arguments}. Got: {fun_arg_count}."
                                             f" Line: {ctx.stop.line}")
        elif ctx.arg_list_include_scope():  # assignment
            n_values_to_assign = len(ctx.arg_list_include_scope().arg_name())
            if n_values_to_assign != ret_arg_count:
                self.error.errors.append(f"Cannot unpack {n_values_to_assign} objects to {ret_arg_count} objects. "
                                         f"Line: {ctx.stop.line}")
        else:  # list declaration here
            if ret_arg_count > 1:  # incorrect list declaration
                self.error.errors.append(f"Cannot unpack list to {ret_arg_count} objects. Line: {ctx.stop.line}")

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
        self.register.add_object_to_scope(ctx.NAME(0).getText(), self.current_scope_name)

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def exitProgram(self, ctx: dUMLeParser.ProgramContext):
        for function_name, function_tuples in self.function_descriptors_to_verify.items():
            for function_tuple in function_tuples:
                self.error.errors.append(f"Did not find declaration of \"{function_name}\". Line: {function_tuple[1]}")
