from interpreter.parser import CogentParser, CogentTransformer
from interpreter.semantic_model import CogentModule

def test_module_imports():
    source = '''
    module Main {
        import Utils
        import Math
        goal: "Test imports"
        inputs: []
        process: ["Do something"]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    model = CogentTransformer().transform(tree)
    if hasattr(model, 'children') and model.children:
        model = model.children[0]
    assert isinstance(model, CogentModule)
    assert model.imports == ["Utils", "Math"]
