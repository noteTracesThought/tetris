import game.game_start_and_score as gmstdc
import game.position  as posdc
import block.block_catalog    as blkdc
import board.playboard    as brddc

from settings import OS_ENVIROMENT, LINUX, WINDOWS, KEY_GAME_FINISH, KEY_DROP, KEY_LEFT, KEY_RIGHT, KEY_ROTATION_LEFT, KEY_ROTATION_RIGHT
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
        self.score      = gmstdc.Score()
        self.blocks_map = blkdc.BlockMap()
        self.play_board = brddc.PalyBoard()
        self.pos        = posdc.MovePosition(current=posdc.Position(), next=posdc.Position(),)
        self.blocks     = Blocks(self.pos, self.blocks_map, self.play_board)
        self.input      = Input(self.pos, self.blocks_map, self.blocks)
        self.collision  = Collision(self.pos, self.blocks_map, self.play_board, self.blocks)
        self.renderer   = Renderer()
        self.board      = Board(self.pos, self.blocks_map, self.play_board, self.renderer)
        self.init_game()

    def power_on_game(self):
        '''Start the Tetris game loop.

        Initialize the game and handle
        user input until quit command.

        Returns:
            None
        '''
        print("[task] power on")

        put_key = ""
        block = self.blocks.get_block()
        self.pos.current.x          = gmstdc.GameStart.START_POS_INI_X
        self.pos.current.y          = gmstdc.GameStart.START_POS_INI_Y
        self.blocks_map.rotation    = gmstdc.GameStart.START_ROTATION
        self.score = gmstdc.Score()
        while(put_key != KEY_GAME_FINISH):
        
            if OS_ENVIROMENT == LINUX:
                put_key = self.input.getch_for_Linux()
            elif OS_ENVIROMENT == WINDOWS:
                if msvcrt.kbhit():
                    put_key = msvcrt.getch()
            else:
                put_key = input()

            self.input.request_operation_rotate(put_key, block)
            self.input.get_next_position(put_key)
            if self.collision.is_invalid_position(block):
                self.pos.next.x = self.pos.current.x
                self.pos.next.y = self.pos.current.y

            # 衝突検知
            if self.collision.check_collision_detection(block):
                self.blocks.fix_block(block)  # update board result
                # print(f"x={x}")
                # print(f"y={y}")
                # print(f"next_x={next_x}")
                # print(f"next_y={next_y}")

                # game over
                if self.is_game_over(put_key) == True:
                    print("game over!")
                    break

                # bingo
                bingo_lines = self.board.get_bingo_lines()
                # ▼rev0.3->rev0.4:責務分離のため改修▼
                if bingo_lines:
                    print("bingo!!")
                    # ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
                    # self.score.value += len(bingo_lines)
                    self.score.add(len(bingo_lines))
                    # ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲
                    self.board.clear_bingo_lines()
                # ▲rev0.3->rev0.4:責務分離のため改修▲

                block = self.blocks.get_block()
                # print(block)
                self.pos.current.x          = gmstdc.GameStart.START_POS_INI_X
                self.pos.current.y          = gmstdc.GameStart.START_POS_INI_Y
                self.blocks_map.rotation    = gmstdc.GameStart.START_ROTATION
            else:
                self.pos.current.x = self.pos.next.x
                self.pos.current.y = self.pos.next.y

            # print(rotation)
            # print(block[rotation])
            # print(type(block[rotation]))
            self.board.update_view(block)
        print(f"score : {self.score.value * 100}")

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
            self.pos.next.y = 1
        else:
            self.pos.next.y = 0
        for c in range(len(self.play_board.board_result[self.pos.next.y])):
            if self.play_board.board_result[self.pos.next.y][c] == 1:
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
        print("[init] initialize")
        self.board.init_board()
        self.blocks.create_blocks()
