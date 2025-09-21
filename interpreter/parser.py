"""
Cogent Parser

Agent-centric parser for Cogent source files, built to reflect the formal EBNF grammar.
Outputs a parse tree or semantic model for downstream analysis.
"""


from lark import Token
from lark.tree import Tree
from pathlib import Path

try:
    from lark import Lark, Transformer, v_args
except ImportError:
    Lark = None  # Will raise error if parser is constructed

# If semantic_model.py is in the same directory:
from .semantic_model import CogentModule, InputItem, ProcessStep

class CogentParser:
    def __init__(self, grammar_path="grammar/cogent.ebnf"):
        """
        Initialize the parser with the EBNF grammar.
        """
        self.grammar_path = grammar_path
        self.parser = None
        self._load_grammar()

    def _load_grammar(self):
        if Lark is None:
            raise ImportError("Lark parser library is not installed. Please run 'pip install lark'.")
        grammar_file = Path(self.grammar_path)
        if not grammar_file.exists():
            raise FileNotFoundError(f"Cogent grammar file not found at: {self.grammar_path}")
        with open(grammar_file, "r") as f:
            grammar = f.read()
        # Use 'start' as the entry rule for Lark grammar
        self.parser = Lark(grammar, parser="earley", start="start", keep_all_tokens=True)

    def parse_file(self, file_path, as_semantic_model=False):
        """
        Parse a Cogent .cg file, returning a parse tree or semantic model.
        """
        with open(file_path, "r") as f:
            source_code = f.read()
        return self.parse_string(source_code, as_semantic_model=as_semantic_model)

    def parse_string(self, source_code, as_semantic_model=False):
        """
        Parse Cogent source from a string.
        Returns a Lark parse tree or semantic model.
        """
        if self.parser is None:
            self._load_grammar()
        tree = self.parser.parse(source_code)
        if as_semantic_model:
            return CogentTransformer().transform(tree)
        return tree

# Transformer stub for semantic model integration
from lark import v_args

class CogentTransformer(Transformer):
    """
    Convert parse trees into semantic model objects.
    Extend this class according to Cogent's grammar and semantic model.
    """
    def module(self, items):
        # Collect annotations at the start
        annotations = self._collect_annotations(items)
        idx = len(annotations)
        name = str(items[idx+1]) if len(items) > idx+1 else None
        imports = []
        types = {}
        body = None
        i = idx+3
        # Collect imports
        while i < len(items) and isinstance(items[i], str):
            imports.append(items[i])
            i += 1
        # Collect type and enum decls
        while i < len(items) and (isinstance(items[i], tuple) or isinstance(items[i], dict)):
            if isinstance(items[i], tuple):
                tname, texpr = items[i]
                types[tname] = texpr
            elif isinstance(items[i], dict):
                types.update(items[i])
            i += 1
        if i < len(items) and isinstance(items[i], list):
            body = items[i]
        if name is None or body is None:
            raise ValueError("Could not extract module name and body from parse tree.")
        goal, inputs, context, process, feedback = body + [None] * (5 - len(body))
        return CogentModule(name, goal, inputs, process, context, feedback, imports=imports, types=types, annotations=annotations)

    def type_decl(self, items):
        # items: ['type', Token('IDENTIFIER', ...), '=', TypeExpr]
        name = str(items[1])
        value = items[3]
        return (name, value)

    def enum_decl(self, items):
        # items: ['enum', Token('IDENTIFIER', ...), '{', enum_item, (',' enum_item)*, '}']
        from interpreter.semantic_model import EnumType
        name = str(items[1])
        # items[3:-1] are enum items and commas
        enum_items = [str(i) for i in items[3:-1] if isinstance(i, str) and i != ',']
        return {name: EnumType(name, enum_items)}

    def enum_item(self, items):
        return str(items[0])

    def type_expr(self, items):
        from interpreter.semantic_model import TypeExpr
        name = str(items[0])
        param = items[1] if len(items) > 1 else None
        return TypeExpr(name, param)

    def type_expr_param(self, items):
        # items: ['<', type_expr, '>']
        return items[1]

    def import_decl(self, items):
        # items: [Token('IMPORT', 'import'), Token('IDENTIFIER', ...)]
        return str(items[1])

    def module_body(self, items):
        goal = None
        inputs = None
        context = None
        process = None
        feedback = None
        from interpreter.semantic_model import ProcessStep, ForStep, WhileStep, TryStep
        for item in items:
            if isinstance(item, str):
                if goal is None:
                    goal = item
                elif context is None:
                    context = item
                elif feedback is None:
                    feedback = item
            elif isinstance(item, list):
                if not item:
                    if inputs is None:
                        inputs = []
                    elif process is None:
                        process = []
                elif isinstance(item[0], InputItem):
                    inputs = item
                elif isinstance(item[0], (ProcessStep, ForStep, WhileStep, TryStep)):
                    process = item
        if inputs is None:
            inputs = []
        if process is None:
            process = []
        return [goal, inputs, context, process, feedback]

    @v_args(inline=True)
    def goal_decl(self, *args):
        if len(args) == 2:
            value = args[1]
        elif len(args) == 1:
            value = args[0]
        else:
            value = None
        return value.strip('"') if value else None

    @v_args(inline=True)
    def inputs_decl(self, *args):
        if len(args) == 2:
            value = args[1]
        elif len(args) == 1:
            value = args[0]
        else:
            value = None
        if isinstance(value, list):
            return [v for v in value if not (hasattr(v, 'type') and v.type in {'LSQB', 'RSQB'})]
        else:
            return value if value else []

    def input_list(self, items):
        return [item for item in items if item is not None and not (hasattr(item, 'type') and item.type in {'LSQB', 'RSQB', 'COMMA'})]

    def input_item(self, items):
        print(f"[DEBUG] input_item: {items}")
        annotations = self._collect_annotations(items)
        idx = len(annotations)
        name = str(items[idx])
        type_name = str(items[idx+2]) if len(items) > idx+2 else None
        print(f"[DEBUG] input_item: name={name}, type_name={type_name}, annotations={annotations}")
        return InputItem(name, type_name, annotations=annotations)

    @v_args(inline=True)
    def context_decl(self, *args):
        if len(args) == 2:
            value = args[1]
        elif len(args) == 1:
            value = args[0]
        else:
            value = None
        return value.strip('"') if value else None

    @v_args(inline=True)
    def process_decl(self, *args):
        if len(args) == 2:
            value = args[1]
        elif len(args) == 1:
            value = args[0]
        else:
            value = None
        if isinstance(value, list):
            return [v for v in value if not (hasattr(v, 'type') and v.type in {'LSQB', 'RSQB'})]
        else:
            return value if value else []


    def process_list(self, items):
        steps = [item for item in items if item is not None and not (hasattr(item, 'type') and item.type in {'LSQB', 'RSQB', 'COMMA'})]
        from interpreter.semantic_model import ProcessStep, ForStep, WhileStep, TryStep
        result = []
        for step in steps:
            if isinstance(step, (ProcessStep, ForStep, WhileStep, TryStep)):
                result.append(step)
            elif isinstance(step, str):
                result.append(ProcessStep(step.strip('"')))
        return result

    def process_step(self, items):
        print(f"[DEBUG] process_step: {items}")
        from interpreter.semantic_model import ProcessStep, ForStep, WhileStep, TryStep
        annotations = self._collect_annotations(items)
        idx = len(annotations)
        # Find the first non-annotation tuple
        j = idx
        print(f"[DEBUG] process_step: items before annotation skip: {items}")
        while j < len(items) and isinstance(items[j], tuple) and len(items[j]) == 2:
            print(f"[DEBUG] Skipping annotation tuple at index {j}: {items[j]}")
            j += 1
        if j < len(items):
            print(f"[DEBUG] process_step: main item at index {j}: {items[j]} (type: {type(items[j])})")
        # try-catch: [Token('TRY', 'try'), process_list, Token('CATCH', 'catch'), IDENTIFIER, process_list]
        if j < len(items) and hasattr(items[j], 'type') and items[j].type == 'TRY':
            try_steps = items[j+1]
            if j+4 < len(items) and hasattr(items[j+2], 'type') and items[j+2].type == 'CATCH':
                catch_var = str(items[j+3])
                catch_steps = items[j+4]
                print(f"[DEBUG] TryStep: try_steps={try_steps}, catch_var={catch_var}, catch_steps={catch_steps}, annotations={annotations}")
                return TryStep(try_steps, catch_var, catch_steps, annotations=annotations)
            print(f"[DEBUG] TryStep: try_steps={try_steps}, no catch, annotations={annotations}")
            return TryStep(try_steps, annotations=annotations)
        # for-loop: [Token('FOR', 'for'), IDENTIFIER, Token('IN', 'in'), IDENTIFIER, Token('COLON', ':'), process_list]
        if j+5 < len(items) and hasattr(items[j], 'type') and items[j].type == 'FOR':
            var = str(items[j+1])
            iterable = str(items[j+3])
            steps = items[j+5]
            print(f"[DEBUG] ForStep: var={var}, iterable={iterable}, steps={steps}, annotations={annotations}")
            return ForStep(var, iterable, steps, annotations=annotations)
        # while-loop: [Token('WHILE', 'while'), STRING, Token('COLON', ':'), process_list]
        if j+3 < len(items) and hasattr(items[j], 'type') and items[j].type == 'WHILE':
            condition = items[j+1]
            if hasattr(condition, 'type') and condition.type == 'STRING':
                condition = str(condition)[1:-1]
            else:
                condition = str(condition)
            steps = items[j+3]
            print(f"[DEBUG] WhileStep: condition={condition}, steps={steps}, annotations={annotations}")
            return WhileStep(condition, steps, annotations=annotations)
        # STRING step
        if j < len(items) and (
            (isinstance(items[j], str)) or
            (hasattr(items[j], 'type') and items[j].type == 'STRING')
        ):
            text = items[j] if isinstance(items[j], str) else str(items[j])[1:-1]
            print(f"[DEBUG] ProcessStep: text={text}, annotations={annotations}")
            return ProcessStep(text.strip('"'), annotations=annotations)
        return items[j] if j < len(items) else None

    def annotation(self, items):
        print(f"[DEBUG] annotation: {items}")
        # items: [@, IDENTIFIER, (args...)?]
        name = str(items[1])
        args = []
        if len(items) > 2 and isinstance(items[2], list):
            args = items[2]
        return (name, args)

    def annotation_args(self, items):
        return items

    def annotation_arg(self, items):
        return str(items[0])

    def _collect_annotations(self, items):
        print(f"[DEBUG] _collect_annotations: {items}")
        # Helper: collect annotation tuples from start of items, return as dict
        annotations = {}
        idx = 0
        while idx < len(items) and isinstance(items[idx], tuple) and len(items[idx]) == 2:
            name, args = items[idx]
            annotations[name] = args if args else True
            idx += 1
        return annotations

    def for_loop(self, items):
        # for IDENTIFIER in IDENTIFIER : process_list
        from interpreter.semantic_model import ForStep
        var = str(items[1])
        iterable = str(items[3])
        steps = items[5]
        print(f"[DEBUG] for_loop: var={var}, iterable={iterable}, steps={steps}")
        return ForStep(var, iterable, steps)

    def while_loop(self, items):
        # while STRING : process_list
        from interpreter.semantic_model import WhileStep
        condition = items[1].strip('"')
        steps = items[3]
        print(f"[DEBUG] while_loop: condition={condition}, steps={steps}")
        return WhileStep(condition, steps)

    @v_args(inline=True)
    def feedback_decl(self, *args):
        if len(args) == 2:
            value = args[1]
        elif len(args) == 1:
            value = args[0]
        else:
            value = None
        return value.strip('"') if value else None

    def type_name(self, items):
        # Simplified: just return as string
        return "".join(str(i) for i in items)


    # Additional rules as needed...

# Usage (example):
# parser = CogentParser()
# module = parser.parse_file("examples/decking.cg", as_semantic_model=True)
