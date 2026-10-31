from dataclasses import dataclass
import position_dataclass as posdc

# 定数
class GameStart:
    START_POS_INI_X = 3
    START_POS_INI_Y = 0
    START_ROTATION  = 0

@dataclass
class Score:
    value:int = 0
