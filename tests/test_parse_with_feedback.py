from interpreter.parser import CogentParser

def test_parse_with_feedback():
    source = '''
    module Example {
        goal: "Test feedback"
        inputs: []
        process: ["Step"]
        feedback: "Some feedback"
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    assert tree is not None
