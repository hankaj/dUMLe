from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from compiler.dUMLeParser import dUMLeParser


@dataclass
class Connection:
    source_object_name: str
    destination_object_name: str
    arrow: str
    label: str = ""

    def __init__(self, ctx: dUMLeParser.ConnectionContext):
        self.source_object_name = ctx.name(0).getText()
        self.destination_object_name = ctx.name(1).getText()
        connection_type = ctx.CONNECTION_TYPE().getText()
        if ctx.TEXT():
            self.label = ctx.TEXT()[1:-1]
        if ctx.ARROW():
            self.arrow = str(ctx.ARROW())
        else:
            arrows = {"aggregate": "o--",
                      "inherit": "<|--",
                      "implement": "<|..",
                      "associate": "<--",
                      "depend": "<..",
                      "compose": "*--"}
            self.arrow = arrows[connection_type]

    def generate(self) -> str:
        result = self.source_object_name + " " + self.arrow + " " + self.destination_object_name
        if self.label:
            result += " : " + self.label
        result += "\n"
        return result


class Note:
    def __init__(self, ctx: dUMLeParser.NoteContext):
        self.object_name = ctx.NAME().getText()
        self.note_code = "note left\n"
        for line in ctx.TEXT():
            self.note_code += (line.getText()[1:-1] + "\n")
        self.note_code += "end note\n"

    def generate(self):
        return self.note_code


class Object(ABC):
    def __init__(self):
        self.name = ""
        self.note = None
        self.theme = None  # todo: implement theme
        self.connections = {}

    # todo: move _change_names funtion here and use it while coping arguments

    @abstractmethod
    def _generate(self) -> str:
        ...

    def generate(self) -> str:
        result = ""
        result += self._generate()

        # implement theme here

        if self.note:
            result += self.note.generate()
        return result

    def generate_connections(self, object_names: List[str] = None) -> str:
        result = ""
        if object_names is None:
            for connections in self.connections.values():
                for connection in connections:
                    result += connection.generate()
        else:
            for class_name in object_names:
                if class_name not in self.connections:
                    continue
                for connection in self.connections[class_name]:
                    result += connection.generate()
        return result

    def add_note(self, note: Note) -> None:
        if self.note is not None:
            raise Exception(f"Note is already attached to the object \"{self.name}\"")
        self.note = note

    def add_connection(self, connection: Connection) -> None:
        if self.name != connection.source_object_name:
            raise Exception(f"Source class name is invalid. Expected: {self.name} Got: {connection.source_object_name}")
        if connection.destination_object_name not in self.connections:
            self.connections[connection.destination_object_name] = [connection]
        else:
            self.connections[connection.destination_object_name].append(connection)


class Theme(Object):
    def __init__(self, ctx: dUMLeParser.ThemeContext):
        super().__init__()
        self.values = []
        self.name = str(ctx.NAME()[0])

        for i in range(len(ctx.PARAM_TYPE())):
            self.values.append((ctx.PARAM_TYPE()[i].getText(), ctx.TEXT()[i].getText().replace('"', '')))

    def _generate(self) -> str:
        res = ""
        for i in range(len(self.values)):
            res += 'skinparam ' + str(self.values[i][0]) + ' ' + str(self.values[i][1]) + '\n'
        return res


class UseCase(Object):
    def __init__(self, ctx: dUMLeParser.Use_caseContext):
        super().__init__()
        self.content = []

        if ctx.name()[0]:
            self.themeName = str(ctx.name()[0])

        self.name = str(ctx.NAME()[0])

        for line in ctx.TEXT():
            self.content.append(line)

    def _generate(self):
        res = 'usecase ('
        for i in range(len(self.content)):
            res += str(self.content[i])
        res += ')\n'
        return res


class Block(Object):
    def __init__(self, ctx: dUMLeParser.BlockContext):
        super().__init__()
        self.label = ""

        if ctx.name():
            self.theme_name = str(ctx.name()[0])

        self.name = str(ctx.NAME()[0])

        if ctx.TEXT():
            self.label = str(ctx.TEXT()).replace('"', '')

    def _generate(self):
        res = "block :" + str(self.name) + ":"
        if self.label != "":
            res += ' as ' + self.label
        return res


class Class(Object):
    def __init__(self, ctx: dUMLeParser.Class_declarationContext):
        super().__init__()
        self.class_lines = ctx.class_declaration_line()
        if ctx.name():
            self.theme = str(ctx.name())
        self.name = str(ctx.NAME())

    def _generate(self) -> str:
        result = "class " + self.name + " {\n"
        for class_declaration_line in self.class_lines:
            if class_declaration_line.MODIFIER():
                access_type = {"private": "-", "public": "+", "protected": "#"}
                result += (access_type[str(class_declaration_line.MODIFIER())])
            result += str(class_declaration_line.TEXT())[1:-1] + "\n"

        result += "}\n"
        return result


class Actor(Object):
    def __init__(self, ctx: dUMLeParser.ActorContext):
        super().__init__()
        self.name = ""
        self.label = ""

        if ctx.name():
            # todo: theme is used in object
            self.theme_name = str(ctx.name()[0])
        self.name = str(ctx.NAME()[0])

        if ctx.TEXT():
            self.label = str(ctx.TEXT()).replace('"', '')

    def _generate(self):
        res = "actor :" + str(self.name) + ":"
        if self.label != "":
            res += ' as ' + self.label
        return res


class Package(Object):
    def __init__(self, ctx: dUMLeParser.Package_declarationContext):
        super().__init__()
        self.name = str(ctx.NAME()[0])
        self.names = []
        self.objects = []

    def _generate(self):
        return ""
