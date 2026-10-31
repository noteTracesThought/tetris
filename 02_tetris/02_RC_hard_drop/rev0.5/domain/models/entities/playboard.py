from dataclasses import dataclass, field

@dataclass
class PalyBoard:
    board_result:list   = field(default_factory=list)         # 永続状態
    board:list          = field(default_factory=list)         # 描画用
