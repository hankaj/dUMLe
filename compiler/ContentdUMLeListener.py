from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.register import Register, Scope
from compiler.utils.object import Theme, Actor, UseCase, ClassDeclaration, Connection, Block, Note, Package


class ContentdUMLeListener(dUMLeListener):
    def __init__(self, register: Register):
        self.register = register
        self.current_scope_name = register.global_scope.name
        self.is_in_function = False
        self.current_function_name = ""

    def exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def enterFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        if self.is_in_function:
            raise Exception("Functions cannot be nested")

        self.is_in_function = True
        self.current_function_name = ctx.NAME().getText()
        self.current_scope_name = self.current_function_name

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self.current_scope_name = ctx.NAME().getText()

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self.current_scope_name = ctx.NAME().getText()

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self.current_scope_name = ctx.NAME().getText()

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = False
        self.current_function_name = ""
        self.exit_scope()

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self.exit_scope()

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self.exit_scope()

    def exitSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self.exit_scope()

    def enterActor(self, ctx: dUMLeParser.ActorContext):
        if self.is_in_function:
            actor = Actor(ctx)
            self.register.update_function_in_scope(self.current_function_name, actor.generate(), self.current_scope_name)
        else:
            # todo: add generator for multiple output
            pass

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        if self.is_in_function:
            use_case = UseCase(ctx)
            self.register.update_function_in_scope(self.current_function_name, use_case.generate(), self.current_scope_name)
        else:
            # todo: add generator for multiple output
            pass

    def enterBlock(self, ctx: dUMLeParser.BlockContext):
        if self.is_in_function:
            block = Block(ctx)
            self.register.update_function_in_scope(self.current_function_name, block.generate(), self.current_scope_name)
        else:
            # todo: add generator for multiple output
            pass

    def enterNote(self, ctx: dUMLeParser.NoteContext):
        if self.is_in_function:
            note = Note(ctx)
            self.register.update_function_in_scope(self.current_function_name, note.generate(), self.current_scope_name)
        else:
            # todo: add generator for multiple output
            pass

    def enterConnection(self, ctx: dUMLeParser.ConnectionContext):
        for name in ctx.NAME():
            if not self.register.is_object_in_scope(name.getText(), self.current_scope_name):
                raise Exception("Object \"" + name.getText() + "\" is not declared in scope \"" + self.current_scope_name + "\"")

        if self.is_in_function:
            connection = Connection(ctx)
            self.register.update_function_in_scope(self.current_function_name, connection.generate(), self.current_scope_name)
        else:
            # todo: add generator for multiple output
            pass

    def enterTheme(self, ctx: dUMLeParser.ThemeContext):
        raise Exception("Theme is not yet supported")
        # if self.is_in_function:
        #     theme = Theme(self, ctx)
        #     theme.process()
        #     self.register.scopes[self.current_scope_name].function_register[
        #         self.current_function_name] += theme.generate()
        # else:
        #     # todo: add generator for multiple output
        #     pass

    def enterPackage_declaration(self, ctx: dUMLeParser.Package_declarationContext):
        if self.is_in_function:  # todo: check if proper scope for package objects
            package = Package(ctx)
            self.register.update_function_in_scope(self.current_function_name, package.generate(),
                                                   self.current_scope_name)
        else:
            # todo: add generator for multiple output
            pass

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        if self.is_in_function:
            class_declaration = ClassDeclaration(ctx)
            self.register.update_function_in_scope(self.current_function_name, class_declaration.generate(), self.current_scope_name)
        else:
            # todo: add generator for multiple output
            pass
