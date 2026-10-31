# import domain.models.valueobject.score    as gmstdc
# import domain.models.valueobject.position  as posdc
from block.block import Blocks
from board.board import Board

from domain.models.entities.block_catalog import BlockMap
from domain.models.entities.playboard import PalyBoard
from domain.models.entities.tetromino import Tetromino
from domain.models.valueobject.position import MovePosition, Position, PosX, PosY
from domain.models.entities.scoreboard import ScoreBoard

# ▼▼▼ 処理速度計測（10万回） ▼▼▼
# ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
from settings import OS_ENVIROMENT, LINUX, WINDOWS, KEY_GAME_FINISH, KEY_DROP, KEY_LEFT, KEY_RIGHT, KEY_ROTATION_LEFT, KEY_ROTATION_RIGHT, \
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
from renderer.renderer import Renderer

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
    def __init__(self):
        self.score      = ScoreBoard('test_user')
        self.blocks_map = BlockMap()
        self.play_board = PalyBoard()
        # self.pos        = posdc.MovePosition(current=posdc.Position(), next=posdc.Position(),)
        self.blocks     = Blocks(self.blocks_map, self.play_board)
        # self.blocks     = Blocks(self.pos, self.blocks_map, self.play_board)
        self.movepos    = MovePosition()
        self.tetromino  = Tetromino(self.blocks, self.movepos)
        # self.input      = Input(self.pos, self.blocks_map, self.blocks)
        self.collision  = Collision(self.tetromino, self.blocks_map, self.play_board, self.blocks)
# ▼▼▼ ハードドロップ機能追加 ▼▼▼
        self.input      = Input(self.tetromino, self.blocks_map, self.blocks, self.collision)
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
        self.renderer   = Renderer()
        self.board      = Board(self.tetromino, self.blocks_map, self.play_board, self.renderer)
        self.init_game()

    def power_on_game(self):
        '''Start the Tetris game loop.

        Initialize the game and handle
        user input until quit command.

        Returns:
            None
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[task] power on")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲

        put_key = ""
        # block = self.blocks.get_block()
        block = self.tetromino.get_tetromino()
        # self.pos.current.x          = gmstdc.GameStart.START_POS_INI_X
        # self.pos.current.y          = gmstdc.GameStart.START_POS_INI_Y
        # self.blocks_map.rotation    = gmstdc.GameStart.START_ROTATION
        # self.score = gmstdc.Score()
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
                    put_key = self.input.getch_for_Linux()
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
            # self.input.request_operation_rotate(put_key, block)
            self.input.request_operation_rotate(put_key)
            pos = self.input.get_next_position(put_key)
            self.tetromino.move(pos)
            if self.collision.is_invalid_position(block):
                # self.pos.next.x = self.pos.current.x
                # self.pos.next.y = self.pos.current.y
                pos = self.tetromino.get_position()
                new_position = MovePosition(
                    # current=(Position(PosX(pos.current.x.value),PosY(pos.current.y.value))),
                    # next=(Position(PosX(pos.current.x.value),PosY(pos.current.y.value)))
                    current=pos.current, next=pos.current
                )
                self.tetromino.move(new_position)

            # 衝突検知
            if self.collision.check_collision_detection(block):
                # self.blocks.fix_block(block)  # update board result
                self.tetromino.fix_tetromino()
                # print(f"x={x}")
                # print(f"y={y}")
                # print(f"next_x={next_x}")
                # print(f"next_y={next_y}")

                # ▼▼▼ 処理速度計測（10万回） ▼▼▼
                # # game over
                # if self.is_game_over(put_key) == True:
                #     print('----------------------------------------')
                #     print('  game over!')
                #     print('----------------------------------------')
                #     break
                # ▲▲▲ 処理速度計測（10万回） ▲▲▲

                # bingo
                bingo_lines = self.board.get_bingo_lines()
                # ▼rev0.3->rev0.4:責務分離のため改修▼
                if bingo_lines:
                    print("bingo!!")
                    self.score.add_score(len(bingo_lines))
                    self.board.clear_bingo_lines()
                # ▲rev0.3->rev0.4:責務分離のため改修▲

                # block = self.blocks.get_block()
                # print(block)
                # self.pos.current.x          = gmstdc.GameStart.START_POS_INI_X
                # self.pos.current.y          = gmstdc.GameStart.START_POS_INI_Y
                # self.blocks_map.rotation    = gmstdc.GameStart.START_ROTATION
                self.tetromino.next_tetromino()
                block = self.tetromino.get_tetromino()
            else:
                # self.pos.current.x = self.pos.next.x
                # self.pos.current.y = self.pos.next.y
                pos = self.tetromino.get_position()
                new_position = MovePosition(
                    # current=(Position(PosX(pos.next.x.value),PosY(pos.next.y.value))),
                    # next=(Position(PosX(pos.next.x.value),PosY(pos.next.y.value)))
                    current=pos.next, next=pos.next
                )
                self.tetromino.move(new_position)

            # print(rotation)
            # print(block[rotation])
            # print(type(block[rotation]))
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        #     self.board.update_view(block)
        # # print(f"score : {self.score.value * 100}")
        # print(f'[user_name]\t: {self.score.get_player()}')
        # # ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
        # # print(f'[score]\t\t: {self.score.get_score() * 100}')
        # print(f'[score]\t\t: {self.score.get_score()}')
        # # ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲

    # def get_bingo_lines(self):
    #     delete_rows = []
    #     for r in range(len(self.play_board.board_result)):
    #         for c in range(len(self.play_board.board_result[r])):
    #             if self.play_board.board_result[r][c] != 1:
    #                 break
    #             if c >= brddc.PlayBoardSize.WIDTH-1:
    #                 delete_rows.append(r)
    #                 print("bingo!!")
    #     return delete_rows

    def is_game_over(self, put_key):
        if put_key == KEY_DROP:
            next_y = 1
        else:
            next_y = 0

        pos = self.tetromino.get_position()
        new_position = MovePosition(
            # current=(Position(PosX(pos.current.x.value),PosY(pos.current.y.value))),
            current=pos.current,
            next=(Position(PosX(pos.next.x.value),PosY(next_y)))
        )
        self.tetromino.move(new_position)
        for c in range(len(self.play_board.board_result[next_y])):
            if self.play_board.board_result[next_y][c] == 1:
                return True
        return False

    '''initialize header
    initialize functions
    '''
    def init_game(self):
        '''Initialize game settings.

        Initialize board and block data.

        Returns:
            None
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[init] initialize")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        self.board.init_board()
        self.blocks.create_blocks()
