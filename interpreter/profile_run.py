from interpreter.parser import CogentParser
from interpreter.resource_profiler import profile_parse

# Use a real example file if available, else a minimal string
try:
    with open("examples/decking_analysis.cg") as f:
        code = f.read()
except FileNotFoundError:
    code = '''
    module Example {
        goal: "Profile test"
        inputs: [x: Int]
        process: ["Step"]
    }
    '''

parser = CogentParser(grammar_path="grammar/cogent.ebnf")
result = profile_parse(parser, code)
print(result)
