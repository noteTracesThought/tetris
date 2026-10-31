import settings
# ▼▼▼ 処理速度計測（10万回） ▼▼▼
# ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
from settings import OS_ENVIROMENT, \
                     LINUX, \
                     WINDOWS, \
                     KEY_GAME_FINISH, \
                     KEY_DROP, \
                     BOARD_SIZE_WIDTH, \
                     SCORE_MULTIPLIER, \
                     KEY_LEFT, \
                     KEY_RIGHT, \
                     KEY_ROTATION_LEFT, \
                     KEY_ROTATION_RIGHT, \
                     KEY_HARD_DROP
# ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲
# ▲▲▲ 処理速度計測（10万回） ▲▲▲

from block.block import Blocks
from board.board import Board
from collision.collision import Collision
from input.input import Input

if OS_ENVIROMENT == LINUX:
    import sys
    import termios
    import tty
elif OS_ENVIROMENT == WINDOWS:
    import msvcrt
else:
    # Do Nothing
    pass

'''tetris main task header
tetris main task functions

Todo:
    * 側面衝突検知時は壁扱いとなるように修正すること
    * ブロックが側面の壁に到達しない
    * 周期タスク処理
'''

class Game():
    def power_on_game():
        '''Start the Tetris game loop.

        Initialize the game and handle
        user input until quit command.

        Returns:
            None
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
            # print("[task] power on")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        Game.init_game()

        put_key = ""
        block = Blocks.get_block()
        x = 3
        y = 0
        score = 0
        rotation = 0
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        proc_cnt = 0
        commands = [
        KEY_DROP,
        KEY_LEFT,
        KEY_RIGHT,
        KEY_ROTATION_LEFT,
        KEY_ROTATION_RIGHT,
        KEY_HARD_DROP,
        ]
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        while(put_key != KEY_GAME_FINISH):
            
            # ▼▼▼ 処理速度計測（10万回） ▼▼▼
            if False:
                if OS_ENVIROMENT == LINUX:
                    put_key = Input.getch_for_Linux()
                elif OS_ENVIROMENT == WINDOWS:
                    if msvcrt.kbhit():
                        put_key = msvcrt.getch()
                else:
                    put_key = input()

            else:
                if proc_cnt < 1_000_000:
                    put_key = commands[proc_cnt % 6]
                    proc_cnt += 1
                else:
                    break               # 10万回計測完了
            # ▲▲▲ 処理速度計測（10万回） ▲▲▲
            rotation = Input.request_operation_rotate(put_key, block, x, y, rotation)
            # ▼▼▼ ハードドロップ機能追加 ▼▼▼
            next_x, next_y = Input.get_next_position(put_key, block, x, y, rotation)
            # ▲▲▲ ハードドロップ機能追加 ▲▲▲
            if Collision.is_invalid_position(block, next_x, next_y, rotation):
                next_x = x
                next_y = y

            # 衝突検知
            if Collision.check_collision_detection(block, next_x, next_y, rotation):
                Blocks.fix_block(block, next_x, next_y, rotation)  # update board result
                # print(f"x={x}")
                # print(f"y={y}")
                # print(f"next_x={next_x}")
                # print(f"next_y={next_y}")

                # ▼▼▼ 処理速度計測（10万回） ▼▼▼
                # # game over
                # if Game.is_game_over(put_key) == True:
                #     print("game over!")
                #     break
                # ▲▲▲ 処理速度計測（10万回） ▲▲▲

                # bingo
                bingo_lines = Game.get_bingo_lines()
                # ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
                # score += len(bingo_lines)
                score += len(bingo_lines) * SCORE_MULTIPLIER[len(bingo_lines)]
                # ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲
                Board.clear_bingo_lines()

                block = Blocks.get_block()
                # print(block)
                x = 3
                y = 0
                rotation = 0
            else:
                x = next_x
                y = next_y

            # print(rotation)
            # print(block[rotation])
            # print(type(block[rotation]))
    # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        #     Board.update_view(block, x, y, rotation)
        # print(f"score : {score * 100}")
    # ▲▲▲ 処理速度計測（10万回） ▲▲▲

    '''initialize header
    initialize functions
    '''
    def init_game():
        '''Initialize game settings.

        Initialize board and block data.

        Returns:
            None
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[init] initialize")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        Board.init_board()
        Blocks.create_blocks()

    def get_bingo_lines():
        delete_rows = []
        for r in range(len(settings.board_result)):
            for c in range(len(settings.board_result[r])):
                if settings.board_result[r][c] != 1:
                    break
                if c >= BOARD_SIZE_WIDTH-1:
                    delete_rows.append(r)
                    print("bingo!!")
        return delete_rows

    def is_game_over(put_key):
        if put_key == KEY_DROP:
            next_y = 1
        else:
            next_y = 0
        for c in range(len(settings.board_result[next_y])):
            if settings.board_result[next_y][c] == 1:
                return True
        return False     
