from dataclasses import dataclass
import game.position as posdc

# ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
SCORE_MULTIPLIER = (0, 1, 1.2, 1.5, 2)
# ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲

# 定数
class GameStart:
    START_POS_INI_X = 3
    START_POS_INI_Y = 0
    START_ROTATION  = 0

@dataclass
class Score:
    value:int = 0

    # ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
    def add(self, score):
        earned_points = int(score * SCORE_MULTIPLIER[score])
        self.value += earned_points
    # ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲
    