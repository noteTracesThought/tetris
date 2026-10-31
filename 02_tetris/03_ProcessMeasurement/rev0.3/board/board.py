import settings
from settings import BOARD_SIZE_WIDTH, \
                     BOARD_SIZE_HEIGHT

class Board():
    def update_view(block, x, y, rotation):
        '''Draw block on the board.

        Clear the previous frame and redraw
        the current block position.

        Args:
            block (tuple):
                Tetromino shape data.
            x (int):
                X-coordinate on the board.
            y (int):
                Y-coordinate on the board.
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[view] update_view")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        # view
        # global board
        Board.load_board_result()                   # おばけ(残像)を消す
        for r in range(len(block[rotation])):
            for c in range(len(block[rotation][r])):
                if block[rotation][r][c] == 1:
                    settings.board[y+r][x+c] = 1
                    # print(f"r+y: {r+y}")
                    # print(f"c+x: {c+x}")
        Board.draw_board(settings.board)

    '''board header
    group board functions
    '''
    def init_board():
        '''Initialize the board.

            Create an empty game board.

            Returns:
                None
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[init] init_board")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        Board.create_board()

    def create_board():
        '''Create an empty board.

            Generate a two-dimensional board
            with fixed width and height.

            Returns:
                None
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[init] create_board")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        # global board_result
        # global board
        settings.board_result = [
            [0] * BOARD_SIZE_WIDTH
            for _ in range(BOARD_SIZE_HEIGHT)
        ]
        settings.board = [
            [0] * BOARD_SIZE_WIDTH
            for _ in range(BOARD_SIZE_HEIGHT)
        ]

    def load_board_result():
        '''Restore the drawing board.

            Create a working board from
            the current board_result state.

            Returns:
                None
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[init] load_board_result")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        # global board
        settings.board = []

        for row in settings.board_result:
            settings.board.append(row[:])
        # print(board_result)
        # print(id(board[0]))
        # print(id(board_result[0]))

    def draw_board(board):
        '''Draw the board on the console.

        Display empty cells as "□"
        and blocks as "■".

        Args:
            board (list):
                Board data to draw.

        Returns:
            None
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[proc] draw_board")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        for row in board:
            line = ""

            for cell in row:
                if cell == 0:
                    line += "□"
                else:
                    line += "■"
            print(line)

    def clear_bingo_lines():
        # global board_result
        new_board = []

        for row in settings.board_result:
            if row.count(1) < BOARD_SIZE_WIDTH:
                new_board.append(row)

        while len(new_board) < BOARD_SIZE_HEIGHT:
            new_board.insert(
                0,
                [0] * BOARD_SIZE_WIDTH
            )
        settings.board_result = new_board
