"""
Semantic Model

Provides agent- and human-friendly representations of Cogent modules,
emphasizing explicit goals, inputs, process, and feedback.
"""

class CogentModule:
    def __init__(self, name, goal, inputs, process, context=None, feedback=None):
        self.name = name
        self.goal = goal
        self.inputs = inputs
        self.process = process
        self.context = context
        self.feedback = feedback

    def __repr__(self):
        return f"<CogentModule name={self.name} goal={self.goal}>"

class InputItem:
    def __init__(self, name, type_name):
        self.name = name
        self.type_name = type_name

class ProcessStep:
    def __init__(self, text):
        self.text = text

# Extendable: add provenance, versioning, agent feedback as needed
