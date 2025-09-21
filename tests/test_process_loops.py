from interpreter.parser import CogentParser, CogentTransformer
from interpreter.semantic_model import ProcessStep, ForStep, WhileStep

def test_process_loops():
    source = '''
    module LoopTest {
        goal: "Test loops"
        inputs: [n: Int]
        process: [
            "Initialize",
            for i in items: [
                "Process item",
                while "condition": [
                    "Inner step"
                ]
            ],
            "Finalize"
        ]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    model = CogentTransformer().transform(tree)
    if hasattr(model, 'children') and model.children:
        model = model.children[0]
    process = model.process
    # Check structure
    assert process[0].text == "Initialize"
    assert isinstance(process[1], ForStep)
    assert process[2].text == "Finalize"
    for_step = process[1]
    assert for_step.var == "i"
    assert for_step.iterable == "items"
    assert isinstance(for_step.steps[0], ProcessStep)
    assert for_step.steps[0].text == "Process item"
    assert isinstance(for_step.steps[1], WhileStep)
    while_step = for_step.steps[1]
    assert while_step.condition == "condition"
    assert while_step.steps[0].text == "Inner step"
