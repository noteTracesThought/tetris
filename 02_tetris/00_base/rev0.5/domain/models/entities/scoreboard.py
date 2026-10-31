from dataclasses import dataclass

from domain.models.valueobject.score import Score

@dataclass
class ScoreBoard:
    player_name: str
    
    def __init__(self, player_name:str, score: int = 0):
        self.player_name    = player_name
        self.score          = Score(score)

    def add_score(self, score):
        self.score = Score(self.score.value + score)
    
    def get_score(self):
        return self.score.value
    
    def get_player(self):
        return self.player_name
