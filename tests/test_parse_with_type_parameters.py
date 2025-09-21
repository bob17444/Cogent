from interpreter.parser import CogentParser

def test_parse_with_type_parameters():
    source = '''
    module Example {
        goal: "Test type parameters"
        inputs: [item: List<String>]
        process: ["Step"]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    assert tree is not None
