import board.playboard    as brddc

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
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[view] update_view")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲

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
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[init] init_board")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        self.create_board()

    def create_board(self):
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
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[init] load_board_result")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
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
