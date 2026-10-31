from game.game import Game
import time

'''tetris main task header
tetris main task functions

Todo:
    * 側面衝突検知時は壁扱いとなるように修正すること
    * ブロックが側面の壁に到達しない
    * 周期タスク処理
'''


if __name__ == "__main__":
    # ▼▼▼ 処理速度計測（10万回） ▼▼▼
    start = time.perf_counter()
    # ▲▲▲ 処理速度計測（10万回） ▲▲▲
    Game.power_on_game()
    # ▼▼▼ 処理速度計測（10万回） ▼▼▼
    stop = time.perf_counter()
    print(f'time = {(stop - start) * 1000}ms')
    # ▲▲▲ 処理速度計測（10万回） ▲▲▲
    print("[task] power off")
