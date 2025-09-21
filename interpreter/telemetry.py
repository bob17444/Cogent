"""
Telemetry & Traceability

Stub for logging actions, resource usage, and agent/human feedback.
Core to Cogent's goal of traceable, transparent execution and evolution.
"""

class Telemetry:
    def __init__(self):
        self.events = []

    def log_event(self, event_type, details):
        """
        Log an event for traceability and future feedback loops.
        """
        self.events.append((event_type, details))
