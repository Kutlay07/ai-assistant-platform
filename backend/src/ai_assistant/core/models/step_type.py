from enum import Enum


class StepType(str, Enum):
    RETRIEVE = "retrieve"
    TOOL = "tool"
    LLM = "llm"
    FINAL_RESPONSE = "final_response"