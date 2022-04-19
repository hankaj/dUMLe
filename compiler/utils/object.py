from abc import ABC, abstractmethod


class Object(ABC):
    @abstractmethod
    def __init__(self, listener, ctx):
        self.listener = listener
        self.ctx = ctx

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def generate(self):
        pass


class Note(Object):
    def __init__(self, listener, ctx):
        self.listener = listener
        self.ctx = ctx

    def process(self):
        pass

    def generate(self):
        pass


class Theme(Object):
    def __init__(self, listener, ctx):
        self.listener = listener
        self.ctx = ctx
        self.values = []

    def process(self):
        # name = self.ctx.NAME().getText()
        for i in range(len(self.ctx.PARAM_TYPE())):
            self.values.append((self.ctx.PARAM_TYPE()[i].getText(), self.ctx.TEXT()[i].getText().replace('"', '')))

    def generate(self):
        self.process()
        res = ""
        for i in range(len(self.values)):
            res += 'skinparam ' + str(self.values[i][0]) + ' ' + str(self.values[i][1]) + '\n'
        return res


# done in BasicListener??
class Connection(Object):
    def __init__(self, listener, ctx):
        self.listener = listener
        self.ctx = ctx

    def process(self):
        pass

    def generate(self):
        pass


class UseCase(Object):
    def __init__(self, listener, ctx):
        self.listener = listener
        self.ctx = ctx
        self.names = []
        self.content = []
        self.useCaseName = ""
        self.themeName = ""

    def process(self):
        self.names = str(self.ctx.NAME())

        if len(self.names) == 2:
            self.themeName = self.names[0]
            self.useCaseName = self.names[1]
        else:
            self.useCaseName = self.names[0]

        for line in self.ctx.TEXT():
            self.content.append(line)

    def generate(self):
        self.process()
        res = 'usecase ('
        for i in range(len(self.content)):
            res += str(self.content[i])
        res += ')\n'
        return res


class Block(Object):
    def __init__(self, listener, ctx):
        self.names = []
        self.blockName = ""
        self.themeName = ""
        self.label = ""
        self.listener = listener
        self.ctx = ctx

    def process(self):
        self.names = self.ctx.NAME()

        if len(self.names) == 2:
            self.themeName = str(self.names[0])
            self.blockName = str(self.names[1])
        else:
            self.blockName = str(self.names[0])

        if self.ctx.TEXT():
            self.label = str(self.ctx.TEXT()).replace('"', '')


    def generate(self):
        self.process()
        res = "block :" + str(self.blockName) + ":"
        if self.label != "":
            res += ' as ' + self.label
        return res


class ClassDeclaration(Object):
    def __init__(self, listener, ctx):
        self.listener = listener
        self.ctx = ctx

    def process(self):
        pass

    def generate(self):
        pass


class Actor(Object):
    def __init__(self, listener, ctx):
        self.names = ctx.NAME()
        self.listener = listener
        self.ctx = ctx
        self.actorName = ""
        self.themeName = ""
        self.label = ""

    def process(self):
        if len(self.names) == 2:
            # theme is used in object
            self.actorName = str(self.names[0])
            self.actorName = str(self.names[1])
        else:
            self.actorName = str(self.names[0])

        if self.ctx.TEXT():
            self.label = str(self.ctx.TEXT()).replace('"', '')

    def generate(self):
        self.process()
        res = "actor :" + str(self.actorName) + ":"
        if self.label != "":
            res += ' as ' + self.label
        return res


class Package(Object):
    def __init__(self, listener, ctx):
        self.listener = listener
        self.ctx = ctx
        self.packageName = ""
        self.themeName = ""
        self.names = []
        self.objects = []

    def process(self):
        self.names = self.ctx.NAME()

        pass

    def generate(self):
        pass
