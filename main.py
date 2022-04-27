import sys
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
from compiler.dUMLeLexer import dUMLeLexer
from compiler.dUMLeParser import dUMLeParser
from compiler.ExecutiondUMLeListener import ExecutiondUMLeListener
from compiler.IndexingdUMLeListener import IndexingdUMLeListener
from compiler.ContentdUMLeListener import ContentdUMLeListener
from compiler.ValidatingdUMLeListener import ValidatingdUMLeListener
from compiler.utils.register import Register
from compiler.utils.error_message import ErrorMessage


# def generate_output():
#     outfile = "results/result.png"
#     server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
#     server.processes_file(filename="results/output.txt", outfile=outfile)


def execute_dumle(input_stream):
    # creating objects
    error = ErrorMessage([])
    lexer = dUMLeLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = dUMLeParser(stream)
    tree = parser.program()
    walker = ParseTreeWalker()
    register = Register()

    # validating the code
    indexing_listener = IndexingdUMLeListener(register, error)
    validating_listener = ValidatingdUMLeListener(register, error)
    print("Indexing...")
    walker.walk(indexing_listener, tree)
    print("Validating...")
    walker.walk(validating_listener, tree)
    if error.errors:
        print("Fix the following errors:")
        print(error.errors)
        return

    return  # todo: delete this

    # code execution
    content_listener = ContentdUMLeListener(register)
    execution_listener = ExecutiondUMLeListener(register)
    walker.walk(content_listener, tree)
    walker.walk(execution_listener, tree)

    # generating final result
    generate_output()


def main(argv):
    if len(argv) < 2 or argv[1][-4:] != ".dml":
        raise ValueError("Pass *.dml file as parameter")
    input_file = FileStream(argv[1], encoding="utf-8")
    execute_dumle(input_file)


if __name__ == '__main__':
    main(sys.argv)
