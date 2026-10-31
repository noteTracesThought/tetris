from dataclasses import dataclass, field

@dataclass
class Position:
    x:int = 0
    y:int = 0

@dataclass
class MovePosition:
    current:Position = field(default_factory=Position)  # 現在描画位置
    next:Position = field(default_factory=Position)     # 次フレーム移動先
