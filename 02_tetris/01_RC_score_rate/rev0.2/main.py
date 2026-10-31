from game.game import power_on_game

'''tetris main task header
tetris main task functions

Todo:
    * 側面衝突検知時は壁扱いとなるように修正すること
    * ブロックが側面の壁に到達しない
    * 周期タスク処理
'''

if __name__ == "__main__":
    power_on_game()
    print("[task] power off")
