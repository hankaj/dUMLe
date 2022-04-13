from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.register import Register



class IndexingdUMLeListener(dUMLeListener):
    def __init__(self, register: Register):
        self.register = register
        self.current_scope_name = 'global'

    def enterFun_declaraion(self, ctx:dUMLeParser.Fun_declaraionContext):
        self.register.add_function_to_scope(ctx.NAME().getText(), "", self.current_scope_name) # todo add try block
        # self.current_scope_name =

    def enterObj_declaration(self, ctx:dUMLeParser.Obj_declarationContext):
        pass
