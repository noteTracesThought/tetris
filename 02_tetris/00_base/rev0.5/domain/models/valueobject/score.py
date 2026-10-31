from dataclasses import dataclass

MAX = 2_147_483_647 # MAX(仮)

@dataclass(frozen=True, slots=True)
class Score:
    value: int
    def __post_init__(self):
        if not (0 <= self.value < MAX):
            raise ValueError("Max Score out of range")
