from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.object import Theme, Actor, UseCase
from compiler.utils.register import Register


class BasicdUMLeListener(dUMLeListener):
    def __init__(self, register: Register):
        self.is_in_class_diag = False
        self.is_in_class = False
        self.output = ""
        self.themes = {}
        self.register = register

    def update_output(self, string_to_add):
        self.output += string_to_add

    def enterProgram(self, ctx:dUMLeParser.ProgramContext):
        self.update_output("@startuml\n")

    def exitProgram(self, ctx:dUMLeParser.ProgramContext):
        self.update_output("@enduml")
        with open("results/output.txt", 'w+') as fp:
            fp.write(self.output.rstrip())

    # global

    def enterTheme(self, ctx:dUMLeParser.ThemeContext):
        if str(ctx.NAME()) in self.themes.keys():
            raise Exception("This theme is already declared") # todo: add proper exception

        theme = Theme(self, ctx)
        theme_code = theme.generate()
        # todo: implement theme here
        self.themes[str(ctx.NAME())] = theme_code
        self.update_output(theme_code)

    def exitTheme(self, ctx:dUMLeParser.ThemeContext):
        pass

    # diagram functions

    def enterClass_diagram(self, ctx:dUMLeParser.Class_diagramContext):
        # todo: split the output here
        pass

    def exitClass_diagram(self, ctx:dUMLeParser.Class_diagramContext):
        # todo: end split the output here
        pass

    # object delaration functions

    def enterClass_declaration(self, ctx:dUMLeParser.Class_declarationContext):
        # todo set in function flag
        # todo: deal with themes here
        names = ctx.NAME()
        self.update_output(ctx.CLASS_TYPE().getText() + " " + str(names[-1]) + "{\n")

    def exitClass_declaration(self, ctx:dUMLeParser.Class_declarationContext):
        self.update_output("}\n")

    def enterClass_declaration_line(self, ctx:dUMLeParser.Class_declaration_lineContext):
        if ctx.MODIFIER():
            type = {"private": "-", "public": "+", "protected": "#"}
            self.update_output(type[str(ctx.MODIFIER())])
        self.update_output(str(ctx.TEXT())[1:-1] + "\n")

    def exitClass_declaration_line(self, ctx:dUMLeParser.Class_declaration_lineContext):
        # todo: delete this ?
        pass

    def enterConnection(self, ctx:dUMLeParser.ConnectionContext):
        # todo: set flag? delete this ?
        pass

    def exitConnection(self, ctx:dUMLeParser.ConnectionContext): # connection is ready
        names = ctx.NAME()
        if ctx.ARROW():
            arrow = str(ctx.ARROW())
        else:
            arrows = {"aggregate": "o--",
                    "inherit": "<|--",
                    "implement": "<|..",
                    "associate": "<--",
                    "depend": "<..",
                    "compose": "*--"}
            arrow = arrows[ctx.CONNECTION_TYPE().getText()]

        self.update_output(str(names[0]) + " " + arrow + " " + str(names[1]))

        if ctx.TEXT():
            self.update_output(" : " + str(ctx.TEXT())[1:-1])

        self.update_output("\n")

    def exitNote(self, ctx:dUMLeParser.NoteContext):
        self.update_output("note left\n")
        for line in ctx.TEXT():
            self.update_output("  " + line.getText()[1:-1] + "\n")
        self.update_output("end note\n")

    # Enter a parse tree produced by dUMLeParser#actor.
    def enterActor(self, ctx:dUMLeParser.ActorContext):
        actor = Actor(self, ctx)
        actor_code = actor.generate()
        self.update_output(actor_code + '\n')

    # Exit a parse tree produced by dUMLeParser#actor.
    def exitActor(self, ctx:dUMLeParser.ActorContext):
        pass

        # Enter a parse tree produced by dUMLeParser#use_case.

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        useCase = UseCase(self,ctx)
        useCase_code = useCase.generate()
        self.update_output(useCase_code)
        pass
