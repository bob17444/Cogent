from interpreter.parser import CogentParser

def test_parse_multiple_modules():
    source = '''
    module First {
        goal: "First goal"
        inputs: []
        process: ["Step1"]
    }
    module Second {
        goal: "Second goal"
        inputs: [x: Int]
        process: ["Step2"]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    assert tree is not None
