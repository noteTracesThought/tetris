import settings
from settings import(
    BOARD_SIZE_WIDTH,
    BOARD_SIZE_HEIGHT
)
# WindowsのコマンドプロンプトでANSI入出力を有効化（必要に応じて自動適用されます）

import sys
import os
os.system('')
# 画面全体をクリアする
os.system('clear')

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
    # print("[view] update_view")

    # view
    global board
    load_board_result()                   # おばけ(残像)を消す
    current_block = block[rotation]
    for r in range(len(current_block)):
        for c in range(len(current_block[r])):
            if current_block[r][c] != 1:
                continue

            settings.board[y + r][x + c] = 1
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
    # print("[init] init_board")
    create_board()

def create_board():
    '''Create an empty board.

        Generate a two-dimensional board
        with fixed width and height.

        Returns:
            None
    '''
    # print("[init] create_board")
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
    # print("[init] load_board_result")
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
    # print("[proc] draw_board")
    move_up(20)
    output_lines = []
    for row in board:
        line = ""

        for cell in row:
            if cell == 0:
                line += "□"
            else:
                line += "■"
        # print(line)
        output_lines.append(line)
    # # 画面に出力
    # sys.stdout.write("\n".join(output_lines) + "\n")
    # sys.stdout.flush()

    # カーソルを盤面の先頭へ移動
    # 例：盤面が20行なら20行上へ移動
    sys.stdout.write("\033[20A")

    # 同じ位置から盤面を再描画
    for line in output_lines:
        # 行をクリアしてから描画
        sys.stdout.write("\033[2K")
        sys.stdout.write(line)
        sys.stdout.write("\n")

    sys.stdout.flush()

# カーソルを上に移動させる関数
def move_up(lines):
    sys.stdout.write(f"\033[{lines}A")

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
