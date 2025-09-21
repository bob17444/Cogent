from interpreter.parser import CogentParser, CogentTransformer, ProcessStep
from interpreter.semantic_model import TryStep

def test_process_try_catch():
    source = '''
    module TryTest {
        goal: "Test try/catch"
        inputs: []
        process: [
            try [
                "Try step 1",
                "Try step 2"
            ] catch err [
                "Catch step 1",
                "Catch step 2"
            ]
        ]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    print("[DEBUG] Parse tree:", tree)
    model = CogentTransformer().transform(tree)
    print("[DEBUG] Model:", model)
    if hasattr(model, 'children') and model.children:
        model = model.children[0]
    process = model.process
    print("[DEBUG] Process steps:", process)
    if process:
        print("[DEBUG] First process step type:", type(process[0]))
        if isinstance(process[0], TryStep):
            print("[DEBUG] TryStep.try_steps:", process[0].try_steps)
            print("[DEBUG] TryStep.catch_var:", process[0].catch_var)
            print("[DEBUG] TryStep.catch_steps:", process[0].catch_steps)
    assert isinstance(process[0], TryStep)
    assert isinstance(process[0].try_steps[0], ProcessStep)
    assert process[0].try_steps[0].text == "Try step 1"
    assert process[0].catch_var == "err"
    assert process[0].catch_steps[1].text == "Catch step 2"
