from interpreter.parser import CogentParser, CogentTransformer
from interpreter.semantic_model import CogentModule

def test_semantic_model_multiple_modules():
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
    # Lark returns a list for start rule with multiple modules
    models_tree = CogentTransformer().transform(tree)
    # Lark returns a Tree for the start rule; extract all CogentModule children
    if hasattr(models_tree, 'children'):
        models = [m for m in models_tree.children if isinstance(m, CogentModule)]
    else:
        models = [models_tree] if isinstance(models_tree, CogentModule) else []
    assert len(models) == 2
    assert models[0].name == "First"
    assert models[1].name == "Second"
    assert models[1].inputs[0].name == "x"
    assert models[1].inputs[0].type_name == "Int"
