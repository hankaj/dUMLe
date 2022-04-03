from dUMLeListener import dUMLeListener
from dUMLeParser import dUMLeParser


class BasicdUMLeListner(dUMLeListener):
    def __init__(self):
        # dict = {"App": {"dmfldfmsd"}}      App -> {  Game_Player_Inherit -> {"plantuml code"},  Player->{"plantuml"}  ... }
        self.is_in_class_diag = False
        self.is_in_class = False
        self.output = ""

    def update_output(self, string_to_add):
        self.output += string_to_add

    def enterProgram(self, ctx:dUMLeParser.ProgramContext):
        self.update_output("@startuml\n")

    def exitProgram(self, ctx:dUMLeParser.ProgramContext):
        self.update_output("@enduml")
        with open("output.txt", 'w+') as fp:
            fp.write(self.output.rstrip())
        # todo: send the output to the server

    def enterClass_diagram(self, ctx:dUMLeParser.Class_diagramContext):
        # todo: split the output here
        pass

    def exitClass_diagram(self, ctx:dUMLeParser.Class_diagramContext):
        # todo: end split the output here
        pass

    def enterClass_declaration(self, ctx:dUMLeParser.Class_declarationContext):
        # todo set in function flag
        pass

    def exitClass_declaration(self, ctx:dUMLeParser.Class_declarationContext):
        names = ctx.NAME()
        # todo: deal with themes here
        self.update_output("class " + str(names[-1]) + "{\n")
        # todo: deal with access here
        print(ctx.MODIFIER(1).getText())
        for line in ctx.TEXT():
            self.update_output(str(line)[1:-1] + "\n")

        self.update_output("}\n")

    # Enter a parse tree produced by dUMLeParser#connection.
    def enterConnection(self, ctx:dUMLeParser.ConnectionContext):
        # todo: set flag?
        pass

    # Exit a parse tree produced by dUMLeParser#connection.
    def exitConnection(self, ctx:dUMLeParser.ConnectionContext):
        names = ctx.NAME()
        # todo: implement label here
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
            #arrow = arrows[ctx.connection_type().getText()]

        self.update_output(str(names[0]) + " " + arrow + " " + str(names[1]) + "\n")

