from interpreter.parser import CogentParser, CogentTransformer
from interpreter.semantic_model import CogentModule, InputItem, ProcessStep
import pytest

def test_semantic_model_empty_inputs_and_process():
    source = '''
    module EmptyTest {
        goal: "Nothing to do"
        inputs: []
        process: []
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    model = CogentTransformer().transform(tree)
    if hasattr(model, 'children') and model.children:
        model = model.children[0]
    assert isinstance(model, CogentModule)
    assert model.name == "EmptyTest"
    assert model.goal == "Nothing to do"
    assert model.inputs == []
    assert model.process == []
    assert model.context is None
    assert model.feedback is None

def test_semantic_model_multiple_inputs_and_steps():
    source = '''
    module MultiTest {
        goal: "Multi input and steps"
        inputs: [a: Int, b: String, c: Float]
        process: ["Step1", "Step2", "Step3"]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    model = CogentTransformer().transform(tree)
    if hasattr(model, 'children') and model.children:
        model = model.children[0]
    assert isinstance(model, CogentModule)
    assert model.name == "MultiTest"
    assert model.goal == "Multi input and steps"
    assert len(model.inputs) == 3
    assert model.inputs[0].name == "a" and model.inputs[0].type_name == "Int"
    assert model.inputs[1].name == "b" and model.inputs[1].type_name == "String"
    assert model.inputs[2].name == "c" and model.inputs[2].type_name == "Float"
    assert len(model.process) == 3
    assert model.process[0].text == "Step1"
    assert model.process[1].text == "Step2"
    assert model.process[2].text == "Step3"
    assert model.context is None
    assert model.feedback is None

def test_semantic_model_with_all_fields():
    source = '''
    module FullTest {
        goal: "All fields"
        inputs: [x: Int]
        context: "Test context"
        process: ["Do something"]
        feedback: "Test feedback"
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    model = CogentTransformer().transform(tree)
    if hasattr(model, 'children') and model.children:
        model = model.children[0]
    assert isinstance(model, CogentModule)
    assert model.name == "FullTest"
    assert model.goal == "All fields"
    assert len(model.inputs) == 1
    assert model.inputs[0].name == "x" and model.inputs[0].type_name == "Int"
    assert model.context == "Test context"
    assert len(model.process) == 1
    assert model.process[0].text == "Do something"
    assert model.feedback == "Test feedback"
