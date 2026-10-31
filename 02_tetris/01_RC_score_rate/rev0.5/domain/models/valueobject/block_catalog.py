from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Rotation:
    value: int

    def __post_init__(self):
        object.__setattr__(self, "value", self.value % 4)   # 4:(上下左右の回転)
