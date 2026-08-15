class StepExecutionError(Exception):
    """Raised when a plan step cannot be executed."""


class MaxIterationsExceededError(Exception):
    """Raised when agent execution exceeds the maximum iteration limit."""