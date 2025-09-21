from interpreter.parser import CogentParser
import pytest

def test_parse_invalid_missing_goal():
    source = '''
    module Example {
        inputs: []
        process: ["Step"]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    with pytest.raises(Exception):
        parser.parse_string(source)
