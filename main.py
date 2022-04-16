import sys
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
from compiler.dUMLeLexer import dUMLeLexer
from compiler.dUMLeParser import dUMLeParser
from compiler.BasicdUMLeListener import BasicdUMLeListener
from compiler.IndexingdUMLeListener import IndexingdUMLeListener
from compiler.utils.register import Register
from plantuml import PlantUML


def generate_output():
    outfile = "results/result.png"
    server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    server.processes_file(filename="results/output.txt", outfile=outfile)


def execute_dumle(input_stream):
    lexer = dUMLeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = dUMLeParser(stream)
    tree = parser.program()
    walker = ParseTreeWalker()
    register = Register()
    indexing_listener = IndexingdUMLeListener(register)
    listener = BasicdUMLeListener()
    walker.walk(indexing_listener, tree)
    walker.walk(listener, tree)
    # print(register.scopes)
    # generate_output()


def main(argv):
    if len(argv) < 2 or argv[1][-4:] != ".dml":
        raise ValueError("Pass *.dml file as parameter")
    input_file = FileStream(argv[1], encoding="utf-8")
    execute_dumle(input_file)


if __name__ == '__main__':
    main(sys.argv)