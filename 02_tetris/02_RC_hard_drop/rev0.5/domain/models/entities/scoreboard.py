from dataclasses import dataclass

from domain.models.valueobject.score import Score

# ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
BASE_SCORE = 100
SCORE_MULTIPLIER = (0, 1, 1.2, 1.5, 2)
# ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲

@dataclass
class ScoreBoard:
    player_name: str
    
    def __init__(self, player_name:str, score: int = 0):
        self.player_name    = player_name
        self.score          = Score(score)

    def add_score(self, lines_cleared: int):
        # ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
        # self.score = Score(self.score.value + score)
        if lines_cleared <= 0:
            return
        
        # 5ライン以上の場合は最大倍率（インデックス4）を適用してエラーを防ぐ
        multiplier_index = min(lines_cleared, len(SCORE_MULTIPLIER) - 1)
        multiplier = SCORE_MULTIPLIER[multiplier_index]
        
        # 基礎点 × ライン数 × 倍率 でスコアを計算
        earned_points = int(BASE_SCORE * lines_cleared * multiplier)
        
        self.score = Score(self.score.value + earned_points)
        # ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲
    
    def get_score(self):
        return self.score.value
    
    def get_player(self):
        return self.player_name
