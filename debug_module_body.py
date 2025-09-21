from interpreter.parser import CogentParser, CogentTransformer
from lark.tree import Tree

source = '''
module Example {
    goal: "Say hello"
    inputs: [user: String]
    process: ["Print 'hello'"]
}
'''
parser = CogentParser(grammar_path="grammar/cogent.ebnf")
tree = parser.parse_string(source)

# Print the module_body children and their transformed values
module_tree = None
for child in tree.children:
    if isinstance(child, Tree) and child.data == 'module':
        module_tree = child
        break
if module_tree:
    for idx, mb_child in enumerate(module_tree.children):
        print(f"module child {idx}: {mb_child} type={type(mb_child)}")
        if isinstance(mb_child, Tree) and mb_child.data == 'module_body':
            for j, field in enumerate(mb_child.children):
                print(f"  module_body child {j}: {field} type={type(field)}")
                if isinstance(field, Tree):
                    value = CogentTransformer().transform(field)
                    print(f"    transformed: {value} type={type(value)}")
