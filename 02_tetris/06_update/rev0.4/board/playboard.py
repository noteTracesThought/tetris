from dataclasses import dataclass, field


@dataclass
class PlayBoard:
    board_result:list   = field(default_factory=list)         # 永続状態
    board:list          = field(default_factory=list)         # 描画用

class PlayBoardSize:
    HEIGHT:int = 20      # board height
    WIDTH:int  = 10      # board width