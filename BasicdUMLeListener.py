from dUMLeListener import dUMLeListener
from dUMLeParser import dUMLeParser

class BasicdUMLeListner(dUMLeListener):
    def __init__(self):
        pass


    def exitStart(self, ctx: dUMLeParser.ProgramContext):
        pass
        # with open("output.txt", 'w+') as fp:
        #     fp.write(self.output.rstrip())
