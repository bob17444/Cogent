# Error handling step
class TryStep:
    def __init__(self, try_steps, catch_var=None, catch_steps=None, annotations=None):
        self.try_steps = try_steps
        self.catch_var = catch_var
        self.catch_steps = catch_steps
        self.annotations = annotations or {}
    def __repr__(self):
        if self.catch_var:
            return f"Try {self.try_steps} Catch {self.catch_var}: {self.catch_steps}"
        return f"Try {self.try_steps}"
"""
Semantic Model

Provides agent- and human-friendly representations of Cogent modules,
emphasizing explicit goals, inputs, process, and feedback.
"""



class CogentModule:
    def __init__(self, name, goal, inputs, process, context=None, feedback=None, imports=None, types=None, annotations=None):
        self.name = name
        self.goal = goal
        self.inputs = inputs
        self.process = process
        self.context = context
        self.feedback = feedback
        self.imports = imports or []
        self.types = types or {}
        self.annotations = annotations or {}

    def __repr__(self):
        return f"<CogentModule name={self.name} goal={self.goal} imports={self.imports} types={list(self.types.keys())}>"


class TypeExpr:
    def __init__(self, name, param=None):
        self.name = name
        self.param = param
    def __repr__(self):
        if self.param:
            return f"{self.name}<{self.param}>"
        return self.name

class EnumType:
    def __init__(self, name, items):
        self.name = name
        self.items = items
    def __repr__(self):
        return f"Enum {self.name} {{{', '.join(self.items)}}}"

class InputItem:
    def __init__(self, name, type_name, annotations=None):
        self.name = name
        self.type_name = type_name
        self.annotations = annotations or {}


class ProcessStep:
    def __init__(self, text, annotations=None):
        self.text = text
        self.annotations = annotations or {}

class ForStep:
    def __init__(self, var, iterable, steps, annotations=None):
        self.var = var
        self.iterable = iterable
        self.steps = steps
        self.annotations = annotations or {}
    def __repr__(self):
        return f"For {self.var} in {self.iterable}: {self.steps}"

class WhileStep:
    def __init__(self, condition, steps, annotations=None):
        self.condition = condition
        self.steps = steps
        self.annotations = annotations or {}
    def __repr__(self):
        return f"While {self.condition}: {self.steps}"

# Extendable: add provenance, versioning, agent feedback as needed
