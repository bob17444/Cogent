import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interpreter.parser import CogentParser

def test_parse_minimal_module():
    source = '''
    module Example {
        goal: "Say hello"
        inputs: []
        process: ["Print 'hello'"]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    assert tree is not None
