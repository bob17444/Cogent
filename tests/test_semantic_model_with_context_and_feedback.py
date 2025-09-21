from interpreter.parser import CogentParser, CogentTransformer
from interpreter.semantic_model import CogentModule

def test_semantic_model_with_context_and_feedback():
    source = '''
    module Example {
        goal: "Test context and feedback"
        inputs: []
        context: "This is context."
        process: ["Step"]
        feedback: "This is feedback."
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    model = CogentTransformer().transform(tree)
    if hasattr(model, 'children') and model.children:
        model = model.children[0]
    assert isinstance(model, CogentModule)
    assert model.context == "This is context."
    assert model.feedback == "This is feedback."
