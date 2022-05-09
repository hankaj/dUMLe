import sys
import traceback
from antlr4 import CommonTokenStream, ParseTreeWalker, FileStream
from compiler.dUMLeLexer import dUMLeLexer
from compiler.dUMLeParser import dUMLeParser
from compiler.ExecutiondUMLeListener import ExecutiondUMLeListener
from compiler.IndexingdUMLeListener import IndexingdUMLeListener
from compiler.ContentdUMLeListener import ContentdUMLeListener
from compiler.ValidatingdUMLeListener import ValidatingdUMLeListener
from compiler.FunctionCalldUMLeListener import FunctionCalldUMLeListener
from compiler.utils.register import Register
from compiler.utils.output_generator import OutputGenerator
from compiler.utils.error_message import ErrorMessage


def execute_dumle(input_stream):
    # creating objects
    try:
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

        output_generator = OutputGenerator()

        # code execution
        content_listener = ContentdUMLeListener(register, output_generator)
        function_call_listener = FunctionCalldUMLeListener(register, output_generator)
        execution_listener = ExecutiondUMLeListener(register, output_generator)
        print("Creating content...")
        walker.walk(content_listener, tree)
        print("Calling functions...")
        walker.walk(function_call_listener, tree)
        print("Executing diagrams...")
        walker.walk(execution_listener, tree)

        print("Debug information:")
        output_generator.debug()
    except Exception as e:
        print("Error message: " + str(e))
        traceback.print_exc()

def main(argv):
    if len(argv) < 2 or argv[1][-4:] != ".dml":
        raise ValueError("Pass *.dml file as parameter")
    input_file = FileStream(argv[1], encoding="utf-8")
    execute_dumle(input_file)


if __name__ == '__main__':
    main(sys.argv)
