import settings
# ▼▼▼ 処理速度差比較 ▼▼▼
# from settings import BOARD_SIZE_WIDTH, \
#                      BOARD_SIZE_HEIGHT
from board.playboard import PalyBoard, PlayBoardSize
# ▲▲▲ 処理速度差比較 ▲▲▲

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
                    # ▼▼▼ 処理速度差比較 ▼▼▼
                    # settings.board[y+r][x+c] = 1
                    PalyBoard.board[y+r][x+c] = 1
                    # ▲▲▲ 処理速度差比較 ▲▲▲
                    # print(f"r+y: {r+y}")
                    # print(f"c+x: {c+x}")
        # ▼▼▼ 処理速度差比較 ▼▼▼
        # Board.draw_board(settings.board)
        Board.draw_board(PalyBoard.board)
        # ▲▲▲ 処理速度差比較 ▲▲▲

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
        # ▼▼▼ 処理速度差比較 ▼▼▼
        # settings.board_result = [
        #     [0] * BOARD_SIZE_WIDTH
        #     for _ in range(BOARD_SIZE_HEIGHT)
        # ]
        # settings.board = [
        #     [0] * BOARD_SIZE_WIDTH
        #     for _ in range(BOARD_SIZE_HEIGHT)
        # ]
        PalyBoard.board_result = [
            [0] * PlayBoardSize.WIDTH
            for _ in range(PlayBoardSize.HEIGHT)
        ]
        PalyBoard.board = [
            [0] * PlayBoardSize.WIDTH
            for _ in range(PlayBoardSize.HEIGHT)
        ]
        # ▲▲▲ 処理速度差比較 ▲▲▲

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
        # ▼▼▼ 処理速度差比較 ▼▼▼
        # settings.board = []
        PalyBoard.board = []
        # ▲▲▲ 処理速度差比較 ▲▲▲

        # ▼▼▼ 処理速度差比較 ▼▼▼
        # for row in settings.board_result:
        #     settings.board.append(row[:])
        for row in PalyBoard.board_result:
            PalyBoard.board.append(row[:])
        # ▲▲▲ 処理速度差比較 ▲▲▲
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

        # ▼▼▼ 処理速度差比較 ▼▼▼
        # for row in settings.board_result:
        #     if row.count(1) < BOARD_SIZE_WIDTH:
        #         new_board.append(row)

        # while len(new_board) < BOARD_SIZE_HEIGHT:
        #     new_board.insert(
        #         0,
        #         [0] * BOARD_SIZE_WIDTH
        #     )
        # settings.board_result = new_board
        for row in PalyBoard.board_result:
            if row.count(1) < PlayBoardSize.WIDTH:
                new_board.append(row)

        while len(new_board) < PlayBoardSize.HEIGHT:
            new_board.insert(
                0,
                [0] * PlayBoardSize.WIDTH
            )
        PalyBoard.board_result = new_board
        # ▲▲▲ 処理速度差比較 ▲▲▲
