import random
import gamestart_dataclass  as gmstdc
import position_dataclass   as posdc
import block_dataclass      as blkdc
import board_dataclass      as brddc

WINDOWS           = "Windows"
LINUX             = "Linux"

# -----------------------------------------------
# settings
# -----------------------------------------------
# OS : Windows or Linux
OS_ENVIROMENT      = LINUX      # selection WINDOWS or LINUX

# keyboard
KEY_DROP           = ' '        # 下へ加速
KEY_LEFT           = 's'        # 左へ移動
KEY_RIGHT          = 'd'        # 右へ移動
KEY_ROTATION_RIGHT = 'r'        # ブロックを右回転
KEY_ROTATION_LEFT  = 'w'        # ブロックを左回転
KEY_GAME_FINISH    = 'q'        # ゲームを強制終了させる
# -----------------------------------------------

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
                    self.score.value += len(bingo_lines)
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

class Blocks():
    def __init__(self, pos, blocks_map, play_board):
        self.pos        = pos
        self.blocks_map = blocks_map
        self.play_board = play_board

    def create_blocks(self):
        '''Create tetromino block definitions.

        Initialize block map and key list.

        Returns:
            None
        '''
        print("[init] create_blocks")
        # global blocks_map_key
        # global blocks_map
        self.blocks_map.block_map_key = list()
        self.blocks_map.block_map = {
                        "I": blkdc.I,
                        "J": blkdc.J,
                        "L": blkdc.L,
                        "S": blkdc.S,
                        "Z": blkdc.Z,
                        "O": blkdc.O,
                        "T": blkdc.T,
                    }
        for key in self.blocks_map.block_map.keys():
            self.blocks_map.block_map_key.append(key)

    def get_block(self):
        '''Get a random tetromino block.

        Returns:
            tuple:
                Randomly selected block.
        '''
        return (self.blocks_map.block_map[random.choice(self.blocks_map.block_map_key)])

    def get_block_width(self, block, rotation):
        '''Get effective block width.

        Calculate the actual width of a block
        excluding trailing empty cells.

        Args:
            block (tuple):
                Tetromino shape data.

        Returns:
            int:
                Effective width of the block.
        '''
        print("[check] get_block_width")
        width = 0
        for row in block[rotation]:
            for col in range(len(row)):
                if row[col] == 1:
                    width = max(width, col+1)
        return width

    def get_block_height(self, block, rotation):
        '''Get effective block height.

        Calculate the actual height of a block
        excluding trailing empty cells.

        Args:
            block (tuple):
                Tetromino shape data.

        Returns:
            int:
                Effective height of the block.
        '''
        print("[check] get_block_height")
        height = 0
        for row in range(len(block[rotation])):
            if 1 in block[rotation][row]:
                height = row + 1
        return height

    def check_operation_rotate(self):
        '''Check block rotation validity.

        Validate whether rotation is
        allowed in the current position.

        Returns:
            None
        '''
        print("[check] check_operation_rotate")
        # TODO:
        # Rotation validity check may move to Collision.
        # Current implementation keeps compatibility with rev0.3.
        return False

    def fix_block(self, block):
        '''Fix the block on the board.

            Store the current block into
            board_result as a fixed block.

            Args:
                block (tuple):
                    Current tetromino shape.

            Returns:
                None
        '''
        # global board_result
        for r in range(len(block[self.blocks_map.rotation])):
            for c in range(len(block[self.blocks_map.rotation][r])):
                if block[self.blocks_map.rotation][r][c] == 1:
                    self.play_board.board_result[self.pos.next.y + r][self.pos.next.x + c] = 1
                    # print("check", y+r, x+c)

class Board():
    def __init__(self, pos, blocks_map, play_board, renderer):
        self.pos        = pos
        self.blocks_map = blocks_map
        self.play_board = play_board
        self.renderer   = renderer

    def update_view(self, block):
        '''Draw block on the board.

        Clear the previous frame and redraw
        the current block position.

        Args:
            block (tuple):
                Tetromino shape data.
        '''
        print("[view] update_view")

        # view
        # global board
        self.load_board_result()                   # おばけ(残像)を消す
        for r in range(len(block[self.blocks_map.rotation])):
            for c in range(len(block[self.blocks_map.rotation][r])):
                if block[self.blocks_map.rotation][r][c] == 1:
                    self.play_board.board[self.pos.current.y + r][self.pos.current.x + c] = 1
                    # print(f"r+y: {r+y}")
                    # print(f"c+x: {c+x}")
        # ▼rev0.3->rev0.4:責務分離のため改修▼
        # self.draw_board(self.play_board.board)
        self.renderer.draw(self.play_board.board)
        # ▲rev0.3->rev0.4:責務分離のため改修▲

    '''board header
    group board functions
    '''
    def init_board(self):
        '''Initialize the board.

            Create an empty game board.

            Returns:
                None
        '''
        print("[init] init_board")
        self.create_board()

    def create_board(self):
        '''Create an empty board.

            Generate a two-dimensional board
            with fixed width and height.

            Returns:
                None
        '''
        print("[init] create_board")
        # global board_result
        # global board
        self.play_board.board_result = [
            [0] * brddc.PlayBoardSize.WIDTH
            for _ in range(brddc.PlayBoardSize.HEIGHT)
        ]
        self.play_board.board = [
            [0] * brddc.PlayBoardSize.WIDTH
            for _ in range(brddc.PlayBoardSize.HEIGHT)
        ]

    def load_board_result(self):
        '''Restore the drawing board.

            Create a working board from
            the current board_result state.

            Returns:
                None
        '''
        print("[init] load_board_result")
        # global board
        self.play_board.board = []

        for row in self.play_board.board_result:
            self.play_board.board.append(row[:])
        # print(board_result)
        # print(id(board[0]))
        # print(id(board_result[0]))

    # def draw_board(self, board):
    #     '''Draw the board on the console.

    #     Display empty cells as "□"
    #     and blocks as "■".

    #     Args:
    #         board (list):
    #             Board data to draw.

    #     Returns:
    #         None
    #     '''
    #     print("[proc] draw_board")
    #     for row in board:
    #         line = ""

    #         for cell in row:
    #             if cell == 0:
    #                 line += "□"
    #             else:
    #                 line += "■"
    #         print(line)

    def clear_bingo_lines(self):
        # global board_result
        new_board = []

        for row in self.play_board.board_result:
            if row.count(1) < brddc.PlayBoardSize.WIDTH:
                new_board.append(row)

        while len(new_board) < brddc.PlayBoardSize.HEIGHT:
            new_board.insert(
                0,
                [0] * brddc.PlayBoardSize.WIDTH
            )
        self.play_board.board_result = new_board

    def get_bingo_lines(self):
        delete_rows = []
        for r in range(len(self.play_board.board_result)):
            for c in range(len(self.play_board.board_result[r])):
                if self.play_board.board_result[r][c] != 1:
                    break
                if c >= brddc.PlayBoardSize.WIDTH-1:
                    delete_rows.append(r)
                    # print("bingo!!")
        return delete_rows


class Input():
    '''user input header
    user input functions

    Todo:
        * rotate
    '''

    def __init__(self, pos, blocks_map, blocks):
        self.pos = pos
        self.blocks_map = blocks_map
        self.blocks = blocks

    def getch_for_Linux(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        return ch

    def request_operation_rotate(self, put_key, block):
        '''Handle user input for block movement and rotation.

        Args:
            put_key (str):
                User keyboard input.
            block (tuple):
                Current tetromino shape.

        Returns:
            None
        '''
        print("[req] request_operation_rotate")
        if put_key == KEY_ROTATION_LEFT:
            self.blocks_map.rotation = self.request_operation_rotate_left(block)
        if put_key == KEY_ROTATION_RIGHT:
            self.blocks_map.rotation = self.request_operation_rotate_right(block)

    def get_next_position(self, put_key):
        '''Handle user input for block movement.

        Args:
            put_key (str):
                User keyboard input.

        Returns:
            None

        '''
        print("[req] get_next_position")
        self.pos.next.x = self.pos.current.x
        self.pos.next.y = self.pos.current.y

        if put_key == KEY_RIGHT:
            self.pos.next.x += 1
        elif put_key == KEY_LEFT:
            self.pos.next.x -= 1
        elif put_key == KEY_DROP:
            self.pos.next.y += 1
        else:
            # Do Nothing
            pass

    def request_operation_rotate_left(self, block):
        '''Rotate block to the left.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            tuple:
                Updated block, x-coordinate, and y-coordinate.
        '''
        print("[req] request_operation_rotate_left")
        new_rotation = self.blocks_map.rotation - 1
        if new_rotation < 0:
            new_rotation = 3
        
        block_width = self.blocks.get_block_width(block, new_rotation)
        block_height = self.blocks.get_block_height(block, new_rotation)
        if self.pos.current.x + block_width < 0:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.x + block_width > brddc.PlayBoardSize.WIDTH:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.y + block_height < 0:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.y + block_height > brddc.PlayBoardSize.HEIGHT:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = self.blocks_map.rotation

        return new_rotation

    def request_operation_rotate_right(self, block):
        '''Rotate block to the right.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            tuple:
                Updated block, x-coordinate, and y-coordinate.
        '''
        print("[req] request_operation_rotate_right")
        new_rotation = self.blocks_map.rotation + 1
        new_rotation = new_rotation % 4

        block_width = self.blocks.get_block_width(block, new_rotation)
        block_height = self.blocks.get_block_height(block, new_rotation)
        if self.pos.current.x + block_width< 0:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.x + block_width >= brddc.PlayBoardSize.WIDTH:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.y + block_height< 0:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.y + block_height >= brddc.PlayBoardSize.HEIGHT:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = self.blocks_map.rotation

        return new_rotation

class Collision():
    '''update check header
    update check functions

    Todo:
        * rotate
    '''
    def __init__(self, pos, blocks_map, play_board, Blocks):
        self.pos        = pos
        self.blocks_map = blocks_map
        self.play_board = play_board
        self.blocks     = Blocks

    def is_invalid_position(self, block):
        '''Validate block movement and rotation.

        Correct coordinates to prevent
        movement outside the board.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            tuple:
                Corrected x-coordinate
                and y-coordinate.
        '''
        print("[check] is_invalid_position")
        is_invalid = False
        is_invalid_move = self.is_out_of_board(block)
        is_invalid_rotate = self.blocks.check_operation_rotate()
        if is_invalid_move or is_invalid_rotate:
            is_invalid = True
        return is_invalid

    def is_out_of_board(self, block):
        '''Check movable range of the block.

        Prevent block movement outside
        the board boundary.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            (bool)
                True  : Under or Over
                False : Within the specified range
        '''
        print("[check] is_out_of_board")
        is_invalid = False
        block_width = self.blocks.get_block_width(block, self.blocks_map.rotation)
        block_height = self.blocks.get_block_height(block, self.blocks_map.rotation)
        if self.pos.next.x < 0:
            is_invalid = True
        if self.pos.next.y < 0:
            is_invalid = True
        if self.pos.next.x > brddc.PlayBoardSize.WIDTH - block_width:
            is_invalid = True
        if self.pos.next.y > brddc.PlayBoardSize.HEIGHT - block_height:
            is_invalid = True
        return is_invalid

    def check_collision_detection(self, block):
        '''Check if there was a collision with a block.

        Detecting Block Collisions.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            tuple:
                Corrected x-coordinate
                and y-coordinate.
        '''
        print("[check] check_collision_detection")
        block_width = self.blocks.get_block_width(block, self.blocks_map.rotation)
        block_height = self.blocks.get_block_height(block, self.blocks_map.rotation)
        for r in range(len(block[self.blocks_map.rotation])):
            for c in range(len(block[self.blocks_map.rotation][r])):
                # 衝突検知(床)
                if self.pos.next.y >= brddc.PlayBoardSize.HEIGHT - block_height:
                    # print(f"next_y:{next_y}")
                    return True
                
                # next(blockなし)
                if block[self.blocks_map.rotation][r][c] != 1:
                    continue
                
                # 衝突検知(board block)
                if self.play_board.board_result[self.pos.next.y + r][self.pos.next.x + c] == 1:
                    # print(f"next_y+r:{next_y+r}")
                    # print(f"next_x+c:{next_x+c}")
                    return True
                
                # 衝突検知(next board block)
                if self.play_board.board_result[self.pos.next.y + r + 1][self.pos.next.x + c] == 1:
                    # print(f"next_y+r+1:{next_y+r+1}")
                    # print(f"next_x+c:{next_x+c}")
                    return True
                
        return False

class Renderer():
    def __init__(self):
        pass

    def draw(self, board):
    # def draw_board(self, board):
        '''Draw the board on the console.

        Display empty cells as "□"
        and blocks as "■".

        Args:
            board (list):
                Board data to draw.

        Returns:
            None
        '''
        print("[proc] draw_board")
        for row in board:
            line = ""

            for cell in row:
                if cell == 0:
                    line += "□"
                else:
                    line += "■"
            print(line)


if __name__ == "__main__":
    game = Game()
    game.power_on_game()
    print("[task] power off")
