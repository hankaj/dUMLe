from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.object import Theme, Actor, UseCase, ClassDeclaration, Connection, Block, Note, Package
from compiler.utils.register import Register


class ExecutiondUMLeListener(dUMLeListener):
    def __init__(self, register: Register):
        self.is_in_function = False
        self.themes = {}
        self.output = ""
        self.register = register
        self.current_scope_name = self.register.global_scope.name

    def update_output(self, string_to_add):
        self.output += string_to_add

    def enterProgram(self, ctx: dUMLeParser.ProgramContext):
        self.update_output("@startuml\n")

    def exitProgram(self, ctx: dUMLeParser.ProgramContext):
        self.update_output("@enduml")
        with open("results/output.txt", 'w+') as fp:
            fp.write(self.output.rstrip())

    def exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    # global

    def enterTheme(self, ctx: dUMLeParser.ThemeContext):
        theme = Theme(ctx)
        theme_code = theme.generate()
        self.themes[str(ctx.NAME())] = theme_code
        self.update_output(theme_code)

    # function

    def enterFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        if self.is_in_function:
            raise Exception("Functions cannot be nested")

        self.is_in_function = True

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = False

    def enterFun_call(self, ctx: dUMLeParser.Fun_callContext):
        fun_name = ctx.NAME().getText()
        if not self.register.is_function_in_scope(fun_name, self.current_scope_name):
            raise Exception(
                "Function \"" + fun_name + "\" is not declared in scope \"" + self.current_scope_name + "\"")

        self.update_output(self.register.get_function_body_in_scope(fun_name, self.current_scope_name))

    # diagram

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self.current_scope_name = ctx.NAME().getText()

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self.current_scope_name = ctx.NAME().getText()

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self.current_scope_name = ctx.NAME().getText()

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self.exit_scope()

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self.exit_scope()

    def exitSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self.exit_scope()

    # object delaration functions

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        if not self.is_in_function:
            class_declaration = ClassDeclaration(ctx)
            self.update_output(class_declaration.generate())

    def enterConnection(self, ctx: dUMLeParser.ConnectionContext):
        if not self.is_in_function:
            for name in ctx.NAME():
                if not self.register.is_object_in_scope(name.getText(), self.current_scope_name):
                    raise Exception(
                        "Object \"" + name.getText() + "\" is not declared in scope \"" + self.current_scope_name + "\"")
            connection = Connection(ctx)
            self.update_output(connection.generate() + '\n')

    def exitNote(self, ctx: dUMLeParser.NoteContext):
        self.update_output("note left\n")
        for line in ctx.TEXT():
            self.update_output("  " + line.getText()[1:-1] + "\n")
        self.update_output("end note\n")
        pass

    def enterActor(self, ctx: dUMLeParser.ActorContext):
        actor = Actor(ctx)
        actor_code = actor.generate()
        self.update_output(actor_code + '\n')

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        use_case = UseCase(ctx)
        use_case = use_case.generate()
        self.update_output(use_case + '\n')
