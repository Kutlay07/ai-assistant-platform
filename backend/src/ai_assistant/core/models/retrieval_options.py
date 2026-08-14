from dataclasses import dataclass


@dataclass(slots=True)
class RetrievalOptions:
    top_k: int = 5
    candidate_k: int | None = None
    
    def __post_init__(self):
        if self.candidate_k is None:
            self.candidate_k = self.top_k * 2