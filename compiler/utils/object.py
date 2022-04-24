from abc import ABC, abstractmethod

from compiler.dUMLeParser import dUMLeParser

class Object(ABC):
    @abstractmethod
    def __init__(self, ctx: dUMLeParser):
        pass

    @abstractmethod
    def generate(self):
        pass


class Note(Object):
    def __init__(self, ctx: dUMLeParser.NoteContext):
        self.noteCode = "note left\n"
        for line in ctx.TEXT():
            self.noteCode += ("  " + line.getText()[1:-1] + "\n")

    def generate(self):
        self.noteCode += "end note\n"
        return self.noteCode


class Theme(Object):
    def __init__(self, ctx: dUMLeParser.ThemeContext):
        self.values = []

        for i in range(len(ctx.PARAM_TYPE())):
            self.values.append((ctx.PARAM_TYPE()[i].getText(),ctx.TEXT()[i].getText().replace('"', '')))

    def generate(self):
        res = ""
        for i in range(len(self.values)):
            res += 'skinparam ' + str(self.values[i][0]) + ' ' + str(self.values[i][1]) + '\n'
        return res


class Connection(Object):
    def __init__(self, ctx: dUMLeParser.ConnectionContext):
        self.obj1_name = ctx.name()[0]
        self.obj2_name = ctx.name()[1]
        self.arrow = ctx.ARROW()
        self.connection_type = ctx.CONNECTION_TYPE().getText()
        self.content = ctx.TEXT()

    def generate(self):
        result = ""
        if self.arrow:
            arrow = str(self.arrow)
        else:
            arrows = {"aggregate": "o--",
                      "inherit": "<|--",
                      "implement": "<|..",
                      "associate": "<--",
                      "depend": "<..",
                      "compose": "*--"}
            arrow = arrows[self.connection_type]

        result += str(self.obj1_name) + " " + arrow + " " + str(self.obj2_name)

        if self.content:
            result += " : " + str(self.content)[1:-1]

        result += "\n"
        return result


class UseCase(Object):
    def __init__(self, ctx: dUMLeParser.Use_caseContext):
        self.content = []
        self.useCaseName = ""
        self.themeName = ""

        if len(ctx.NAME()) == 2:
            self.themeName = ctx.name()[0]
            self.useCaseName = ctx.NAME()[1]
        else:
            self.useCaseName = ctx.NAME()[0]

        for line in ctx.TEXT():
            self.content.append(line)

    def generate(self):
        res = 'usecase ('
        for i in range(len(self.content)):
            res += str(self.content[i])
        res += ')\n'
        return res


class Block(Object):
    def __init__(self, ctx: dUMLeParser.BlockContext):
        self.themeName = ""
        self.blockName = ""
        self.label = ""

        if len(ctx.NAME()) == 2:
            self.themeName = str(ctx.NAME()[0])
            self.blockName = str(ctx.NAME()[1])
        else:
            self.blockName = str(ctx.NAME()[0])

        if ctx.TEXT():
            self.label = str(ctx.TEXT()).replace('"', '')

    def generate(self):
        res = "block :" + str(self.blockName) + ":"
        if self.label != "":
            res += ' as ' + self.label
        return res


class ClassDeclaration(Object):
    def __init__(self, ctx: dUMLeParser.Class_declarationContext):
        self.theme = ""
        self.name = ""
        self.class_line = ctx.class_declaration_line()

        if len(ctx.NAME()) == 2:
            self.theme = str(ctx.NAME()[0])
            self.name = str(ctx.NAME()[1])
        else:
            self.name = str(ctx.NAME()[0])

    def generate(self):
        result = "class " + self.name + " {\n"
        for class_declaration_line in self.class_line:
            if class_declaration_line.MODIFIER():
                access_type = {"private": "-", "public": "+", "protected": "#"}
                result += (access_type[str(class_declaration_line.MODIFIER())])
            result += str(class_declaration_line.TEXT())[1:-1] + "\n"

        result += "}\n"
        return result


class Actor(Object):
    def __init__(self, ctx: dUMLeParser.ActorContext):
        self.themeName = ""
        self.actorName = ""
        self.label = ""

        if len(ctx.NAME()) == 2:
            # theme is used in object
            self.themeName = str(ctx.NAME()[0])
            self.actorName = str(ctx.NAME()[1])
        else:
            self.actorName = str(ctx.NAME()[0])

        if ctx.TEXT():
            self.label = str(ctx.TEXT()).replace('"', '')

    def generate(self):
        res = "actor :" + str(self.actorName) + ":"
        if self.label != "":
            res += ' as ' + self.label
        return res


class Package(Object):
    def __init__(self, ctx: dUMLeParser.Package_declarationContext):

        self.packageName = ""
        self.themeName = ""
        self.names = []
        self.objects = []

    def generate(self):
        return ""
