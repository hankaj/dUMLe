from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.register import Register, Scope, FunctionDescriptor
from compiler.utils.object import Object, Theme, Actor, UseCase, Class, Connection, Block, Note, Package
from compiler.utils.function_generator import FunctionGenerator
from compiler.utils.output_generator import OutputGenerator
from compiler.utils.diagram_generator import DiagGenerator


class ContentdUMLeListener(dUMLeListener):
    def __init__(self, register: Register, output_generator: OutputGenerator):
        self.register = register
        self.output_generator = output_generator

        self.current_scope_name = register.global_scope.name
        self.is_in_diagram = False
        self.is_in_function = False
        self.current_function_name = ""
        self.current_diagram_name = ""

    def _enter_diag(self, ctx):
        self.is_in_diagram = True
        self.current_diagram_name = ctx.NAME().getText()
        self.current_scope_name = self.current_diagram_name

    def _exit_diag(self):
        self.current_diagram_name = ""
        self.is_in_diagram = False
        self.exit_scope()

    def exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def enterFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = True
        self.current_function_name = ctx.NAME().getText()
        self.current_scope_name = self.current_function_name

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._enter_diag(ctx)

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._enter_diag(ctx)

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._enter_diag(ctx)

    def exitFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = False
        self.current_function_name = ""
        self.exit_scope()

    def exitClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._exit_diag()

    def exitUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._exit_diag()

    def exitSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._exit_diag()

    def enterActor(self, ctx: dUMLeParser.ActorContext):
        actor = Actor(ctx)
        self._add_object(actor)

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        use_case = UseCase(ctx)
        self._add_object(use_case)

    def enterBlock(self, ctx: dUMLeParser.BlockContext):
        block = Block(ctx)
        self._add_object(block)

    def enterNote(self, ctx: dUMLeParser.NoteContext):
        note = Note(ctx)
        # todo: support theme

        if self.is_in_function:
            self.output_generator.get_function(self.register.parent_name(self.current_function_name),
                                               self.current_function_name).add_note(note)
        elif self.is_in_diagram:
            for object in self.output_generator.diagram_generators[self.current_diagram_name]:
                if object.name == note.object_name:
                    object.add_note(note)
                    break
        else:  # global
            self.output_generator.global_objects[note.object_name].add_note(note)

    def enterConnection(self, ctx: dUMLeParser.ConnectionContext):
        connection = Connection(ctx)
        if self.is_in_function:
            self.output_generator.get_function(self.register.parent_name(self.current_function_name),
                                               self.current_function_name).add_connection(connection)
        elif self.is_in_diagram:
            for object in self.output_generator.diagram_generators[self.current_diagram_name]:
                if object.name == connection.source_object_name:
                    object.add_connection(connection)
                    break
        else:  # global
            self.output_generator.global_objects[connection.source_object_name].add_note(connection)

    def enterTheme(self, ctx: dUMLeParser.ThemeContext):
        raise Exception("Theme is not yet supported")

    def enterPackage_declaration(self, ctx: dUMLeParser.Package_declarationContext):
        package = Package(ctx)
        # todo: implement

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        class_object = Class(ctx)
        self._add_object(class_object)
