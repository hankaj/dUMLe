import sys
from antlr4 import *
from dUMLeLexer import dUMLeLexer
from dUMLeParser import dUMLeParser
from BasicdUMLeListener import BasicdUMLeListner
from plantuml import PlantUML


def generate_output():
    outfile = "result.png"
    server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    server.processes_file(filename="output.txt", outfile=outfile)


def execute_dumle(input_file):
    input_stream = FileStream(input_file)
    lexer = dUMLeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = dUMLeParser(stream)
    tree = parser.program()
    walker = ParseTreeWalker()
    listener = BasicdUMLeListner()
    walker.walk(listener, tree)
    generate_output()


def main(argv):
    if len(argv) < 2 or argv[1][-4:] != ".dml":
        raise ValueError("Pass *.dml file as parameter")
    input_file = FileStream(argv[1], encoding="utf-8")
    execute_dumle(input_file)


if __name__ == '__main__':
    main(sys.argv)