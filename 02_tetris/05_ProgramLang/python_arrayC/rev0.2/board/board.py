import array
import settings
from settings import BOARD_SIZE_WIDTH, \
                     BOARD_SIZE_HEIGHT

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
    global board
    load_board_result()                   # おばけ(残像)を消す
    for r in range(len(block[rotation])):
        for c in range(len(block[rotation][r])):
            if block[rotation][r][c] == 1:
                settings.board[y+r][x+c] = 1
                # print(f"r+y: {r+y}")
                # print(f"c+x: {c+x}")
    draw_board(settings.board)

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
    create_board()

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
    # ▼▼▼ list を使用せず、型指定した固定長配列(array.array)で実装 ▼▼▼
    # 行ごとに array.array('i', ...) を持つ tuple で、C言語の int[H][W] を再現する
    settings.board_result = tuple(
        array.array('i', (0,) * BOARD_SIZE_WIDTH)
        for _ in range(BOARD_SIZE_HEIGHT)
    )
    settings.board = tuple(
        array.array('i', (0,) * BOARD_SIZE_WIDTH)
        for _ in range(BOARD_SIZE_HEIGHT)
    )
    # ▲▲▲ list を使用せず、型指定した固定長配列(array.array)で実装 ▲▲▲

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
    # ▼▼▼ list を使用せず、型指定した固定長配列(array.array)で実装 ▼▼▼
    settings.board = tuple(
        array.array('i', row) for row in settings.board_result
    )
    # ▲▲▲ list を使用せず、型指定した固定長配列(array.array)で実装 ▲▲▲
    # print(board_result)
    # print(id(board[0]))
    # print(id(board_result[0]))

def draw_board(board):
    '''Draw the board on the console.

    Display empty cells as "□"
    and blocks as "■".

    Args:
        board (tuple):
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
    # ▼▼▼ list を使用せず、型指定した固定長配列(array.array)で実装 ▼▼▼
    new_board = tuple(
        row for row in settings.board_result
        if row.count(1) < BOARD_SIZE_WIDTH
    )

    while len(new_board) < BOARD_SIZE_HEIGHT:
        new_board = (array.array('i', (0,) * BOARD_SIZE_WIDTH),) + new_board
    # ▲▲▲ list を使用せず、型指定した固定長配列(array.array)で実装 ▲▲▲
    settings.board_result = new_board

def get_bingo_lines():
    # ▼▼▼ list を使用せず、型指定した固定長配列(array.array)で実装 ▼▼▼
    delete_rows = array.array('i')
    # ▲▲▲ list を使用せず、型指定した固定長配列(array.array)で実装 ▲▲▲
    for r in range(len(settings.board_result)):
        for c in range(len(settings.board_result[r])):
            if settings.board_result[r][c] != 1:
                break
            if c >= BOARD_SIZE_WIDTH-1:
                delete_rows.append(r)
                print("bingo!!")
    return delete_rows
