"""
Agent API

Minimal, transparent API for agents to inspect and interact with Cogent modules.
Supports clarity, traceability, and future feedback-driven evolution.
"""

class AgentAPI:
    def __init__(self, semantic_model):
        self.semantic_model = semantic_model

    def get_goal(self):
        """
        Return the goal of the current Cogent module.
        """
        return getattr(self.semantic_model, "goal", None)

    def get_inputs(self):
        """
        Return the declared inputs of the module.
        """
        return getattr(self.semantic_model, "inputs", None)

    def get_process(self):
        """
        Return the process steps of the module.
        """
        return getattr(self.semantic_model, "process", None)

    # Extendable: methods for feedback, self-evolution, module provenance
