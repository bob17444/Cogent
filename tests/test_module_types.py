from interpreter.parser import CogentParser, CogentTransformer
from interpreter.semantic_model import CogentModule, TypeExpr, EnumType

def test_module_types_and_enums():
    source = '''
    module TypesTest {
        type MyInt = Int
        type ListOfInt = List<MyInt>
        enum Color { Red, Green, Blue }
        goal: "Test types"
        inputs: [x: MyInt, y: ListOfInt, c: Color]
        process: ["Do something"]
    }
    '''
    parser = CogentParser(grammar_path="grammar/cogent.ebnf")
    tree = parser.parse_string(source)
    model = CogentTransformer().transform(tree)
    if hasattr(model, 'children') and model.children:
        model = model.children[0]
    assert isinstance(model, CogentModule)
    assert "MyInt" in model.types
    assert isinstance(model.types["MyInt"], TypeExpr)
    assert model.types["MyInt"].name == "Int"
    assert "ListOfInt" in model.types
    assert model.types["ListOfInt"].name == "List"
    assert isinstance(model.types["ListOfInt"].param, TypeExpr)
    assert model.types["ListOfInt"].param.name == "MyInt"
    assert "Color" in model.types
    assert isinstance(model.types["Color"], EnumType)
    assert set(model.types["Color"].items) == {"Red", "Green", "Blue"}
