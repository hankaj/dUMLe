from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.register import Register, Scope


class IndexingdUMLeListener(dUMLeListener):
    def __init__(self, register: Register):
        self.register = register
        self.current_scope_name = register.global_scope.name

    def enterFun_declaration(self, ctx:dUMLeParser.Fun_declarationContext):
        fun_name = ctx.NAME().getText()
        self.register.add_function_to_scope(fun_name, "", self.current_scope_name) # todo add try block
        fun_scope = Scope(fun_name, self.current_scope_name, [], {})
        self.register.scopes[fun_name] = fun_scope
        self.current_scope_name = fun_name

    def exitFun_declaration(self, ctx:dUMLeParser.Fun_declarationContext):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def enterActor(self, ctx:dUMLeParser.ActorContext):
        self.register.add_object_to_scope(ctx.NAME(0).getText(), self.current_scope_name)

    def enterUse_case(self, ctx:dUMLeParser.Use_caseContext):
        self.register.add_object_to_scope(ctx.NAME(0).getText(), self.current_scope_name)

    def enterBlock(self, ctx:dUMLeParser.BlockContext):
        self.register.add_object_to_scope(ctx.NAME(0).getText(), self.current_scope_name)

    def enterNote(self, ctx:dUMLeParser.NoteContext):
        self.register.add_object_to_scope(ctx.NAME(0).getText(), self.current_scope_name)

    def enterTheme(self, ctx:dUMLeParser.ThemeContext):
        self.register.add_object_to_scope(ctx.NAME().getText(), self.current_scope_name)

    def enterPackage_declaration(self, ctx:dUMLeParser.Package_declarationContext):
        self.register.add_object_to_scope(ctx.NAME(0).getText(), self.current_scope_name)

    def enterClass_declaration(self, ctx:dUMLeParser.Class_declarationContext):
        self.register.add_object_to_scope(ctx.NAME(0).getText(), self.current_scope_name)
