from dataclasses import dataclass, field
from domain.constants.playboard import PlayBoardSize

@dataclass(frozen=True, slots=True)
class PosX:
    value: int
    def __post_init__(self):
        if not (0 <= self.value < PlayBoardSize.WIDTH):
            raise ValueError("PosX out of range")

@dataclass(frozen=True, slots=True)
class PosY:
    value: int
    def __post_init__(self):
        if not (0 <= self.value < PlayBoardSize.HEIGHT):
            raise ValueError("PosY out of range")

@dataclass(frozen=True, slots=True)
class Position:
    x:PosX = field(default_factory=lambda: PosX(0))
    y:PosY = field(default_factory=lambda: PosY(0))

    def move_right(self) -> "Position":
        return Position(x=PosX(self.x.value + 1), y=self.y)

    def move_left(self) -> "Position":
        return Position(x=PosX(self.x.value - 1), y=self.y)

    def move_down(self) -> "Position":
        return Position(x=self.x, y=PosY(self.y.value + 1))
    
@dataclass
class MovePosition:
    current:Position = field(default_factory=lambda: Position(PosX(0), PosY(0)))  # 現在描画位置
    next:Position    = field(default_factory=lambda: Position(PosX(0), PosY(0)))  # 次フレーム移動先
