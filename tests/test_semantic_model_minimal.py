from interpreter.parser import CogentParser, CogentTransformer
from interpreter.semantic_model import CogentModule, InputItem, ProcessStep

def test_semantic_model_minimal():
    source = '''
    module Example {
        goal: "Say hello"
        inputs: [user: String]
        process: ["Print 'hello'"]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    model = CogentTransformer().transform(tree)
    # Lark returns a Tree for the start rule; extract the module
    if hasattr(model, 'children') and model.children:
        model = model.children[0]
    assert isinstance(model, CogentModule)
    assert model.name == "Example"
    assert model.goal == "Say hello"
    assert len(model.inputs) == 1
    assert model.inputs[0].name == "user"
    assert model.inputs[0].type_name == "String"
    assert len(model.process) == 1
    assert model.process[0].text == "Print 'hello'"
    assert model.context is None
    assert model.feedback is None
