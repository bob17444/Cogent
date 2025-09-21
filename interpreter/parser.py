"""
Cogent Parser

Agent-centric parser for Cogent source files, built to reflect the formal EBNF grammar.
Outputs a parse tree or semantic model for downstream analysis.
"""

from pathlib import Path

try:
    from lark import Lark, Transformer, v_args
except ImportError:
    Lark = None  # Will raise error if parser is constructed

# If semantic_model.py is in the same directory:
from semantic_model import CogentModule, InputItem, ProcessStep

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
        self.parser = Lark(grammar, parser="earley", start="Module", keep_all_tokens=True)

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
class CogentTransformer(Transformer):
    """
    Convert parse trees into semantic model objects.
    Extend this class according to Cogent's grammar and semantic model.
    """
    def Module(self, items):
        # items: [Identifier, GoalDecl, InputsDecl, (ContextDecl), ProcessDecl, (FeedbackDecl)]
        name = str(items[0])
        goal = items[1]
        inputs = items[2]
        context = items[3] if len(items) > 4 else None
        process = items[-2] if len(items) > 4 else items[3]
        feedback = items[-1] if len(items) > 4 and len(items) == 6 else None
        return CogentModule(name, goal, inputs, process, context, feedback)

    def GoalDecl(self, items):
        return items[0].strip('"')

    def InputsDecl(self, items):
        return items[0]

    def InputList(self, items):
        return items

    def InputItem(self, items):
        name = str(items[0])
        type_name = str(items[1])
        return InputItem(name, type_name)

    def ContextDecl(self, items):
        return items[0].strip('"')

    def ProcessDecl(self, items):
        return items[0]

    def ProcessList(self, items):
        return [ProcessStep(step.strip('"')) for step in items]

    def ProcessStep(self, items):
        return items[0].strip('"')

    def FeedbackDecl(self, items):
        return items[0].strip('"')

    def TypeName(self, items):
        # Simplified: just return as string
        return "".join(str(i) for i in items)

    def Identifier(self, items):
        return "".join(str(i) for i in items)

    # Additional rules as needed...

# Usage (example):
# parser = CogentParser()
# module = parser.parse_file("examples/decking.cg", as_semantic_model=True)
