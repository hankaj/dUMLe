from compiler.dUMLeListener import dUMLeListener
from compiler.dUMLeParser import dUMLeParser
from compiler.utils.register import Register
from compiler.utils.object import Object, Actor, UseCase, Class, Connection, Block, Note
from compiler.utils.function_generator import FunctionGenerator
from compiler.utils.output_generator import OutputGenerator
from compiler.utils.diagram_generator import DiagGenerator, DiagType


class ContentdUMLeListener(dUMLeListener):
    def __init__(self, register: Register, output_generator: OutputGenerator):
        self.register = register
        self.output_generator = output_generator

        self.current_scope_name = register.global_scope.name
        self.is_in_diagram = False
        self.is_in_function = False
        self.current_diagram_type = None
        self.current_function_name = ""
        self.current_diagram_name = ""

    def _enter_diag(self, ctx, diag_type: DiagType):
        self.is_in_diagram = True
        self.current_diagram_name = ctx.NAME().getText()
        self.current_scope_name = self.current_diagram_name
        self.current_diagram_type = diag_type
        self.output_generator.diagram_generators[self.current_diagram_name] = DiagGenerator(diag_type)

    def _exit_diag(self):
        self.current_diagram_name = ""
        self.current_diagram_type = None
        self.is_in_diagram = False
        self.exit_scope()

    def _add_object(self, object: Object):
        if self.is_in_function:
            self.output_generator.get_function(self.register.parent_name(self.current_function_name),
                                               self.current_function_name).fixed_objects.append(object)
        elif self.is_in_diagram:
            # if self.current_diagram_name not in self.output_generator.diagram_generators:
            #     self.output_generator.diagram_generators[self.current_diagram_name].objects = [object]
            # else:
            #     self.output_generator.diagram_generators[self.current_diagram_name].objects.append(object)
            self.output_generator.diagram_generators[self.current_diagram_name].objects.append(object)
        else:  # global
            self.output_generator.global_objects[object.name] = object

    def exit_scope(self):
        self.current_scope_name = self.register.parent_name(self.current_scope_name)

    def enterFun_declaration(self, ctx: dUMLeParser.Fun_declarationContext):
        self.is_in_function = True
        self.current_function_name = ctx.NAME().getText()
        descriptor = self.register.get_function_descriptor_in_scope(self.current_function_name, self.current_scope_name)
        function_generator = FunctionGenerator(descriptor)

        if ctx.arg_list(1):
            function_generator.modifiable_arg_names = [name.getText() for name in ctx.arg_list(0).NAME()]
            function_generator.return_object_names = [name.getText() for name in ctx.arg_list(1).NAME()]
        else:
            function_generator.return_object_names = [name.getText() for name in ctx.arg_list(0).NAME()]
            
        self.output_generator.add_function(self.current_scope_name, self.current_function_name, function_generator)
        self.current_scope_name = self.current_function_name

    def enterClass_diagram(self, ctx: dUMLeParser.Class_diagramContext):
        self._enter_diag(ctx, DiagType.CLASS)

    def enterUse_case_diagram(self, ctx: dUMLeParser.Use_case_diagramContext):
        self._enter_diag(ctx, DiagType.USE_CASE)

    def enterSeq_diagram(self, ctx: dUMLeParser.Seq_diagramContext):
        self._enter_diag(ctx, DiagType.SEQUENCE)

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
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.USE_CASE:
            raise Exception(f"You cannot define actor in {self.current_diagram_type}. Line: {ctx.stop.line}")
        actor = Actor(ctx)
        self._add_object(actor)

    def enterUse_case(self, ctx: dUMLeParser.Use_caseContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.USE_CASE:
            raise Exception(f"You cannot define use case in {self.current_diagram_type}. Line: {ctx.stop.line}")
        use_case = UseCase(ctx)
        self._add_object(use_case)

    def enterBlock(self, ctx: dUMLeParser.BlockContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.SEQUENCE:
            raise Exception(f"You cannot define block in {self.current_diagram_type}. Line: {ctx.stop.line}")
        block = Block(ctx)
        self._add_object(block)

    def enterNote(self, ctx: dUMLeParser.NoteContext):
        note = Note(ctx)

        if self.is_in_function:
            self.output_generator.get_function(self.register.parent_name(self.current_function_name),
                                               self.current_function_name).notes_to_create.append(note)
        elif self.is_in_diagram:
            for object in self.output_generator.diagram_generators[self.current_diagram_name].objects:
                if object.name == note.object_name:
                    object.add_note(note)
                    break
        else:  # global
            self.output_generator.global_objects[note.object_name].add_note(note)

    def enterConnection(self, ctx: dUMLeParser.ConnectionContext):
        if self.is_in_function:
            connection = Connection(ctx)
            self.output_generator.get_function(self.register.parent_name(self.current_function_name),
                                               self.current_function_name).connections_to_create.append(connection)

    def enterTheme(self, ctx: dUMLeParser.ThemeContext):
        raise Exception(f"Theme is not yet supported. Line: {ctx.stop.line}")

    def enterClass_declaration(self, ctx: dUMLeParser.Class_declarationContext):
        if self.current_diagram_type is not None and self.current_diagram_type != DiagType.CLASS:
            raise Exception(f"You cannot define class in {self.current_diagram_type}. Line: {ctx.stop.line}")
        class_object = Class(ctx)
        self._add_object(class_object)
