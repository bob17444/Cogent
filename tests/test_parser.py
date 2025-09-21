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

def test_parse_decking_analysis_module_semantic():
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    with open("examples/decking_analysis.cg") as f:
        source = f.read()
    module = parser.parse_string(source, as_semantic_model=True)
    assert module.name == "DeckingAnalysisTX"
    assert "composite decking" in module.goal
    assert len(module.inputs) == 4
    assert module.context is not None
    assert "Texas" in module.context
    assert len(module.process) == 5
    assert module.feedback is not None
    assert "feedback" in module.feedback.lower()
