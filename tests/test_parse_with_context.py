from interpreter.parser import CogentParser

def test_parse_with_context():
    source = '''
    module Example {
        goal: "Test context"
        inputs: []
        context: "Some context"
        process: ["Step"]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    assert tree is not None
