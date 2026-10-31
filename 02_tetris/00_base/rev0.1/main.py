import random

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

# const
BOARD_SIZE_HEIGHT = 20      # board height
BOARD_SIZE_WIDTH  = 10      # board width

# global
global board_result         # 永続状態
global board                # 描画用
global block_map_key        # block map key
global block_map            # blocks
TOP_I = (
            (1,1,1,1),
            (0,0,0,0),
            (0,0,0,0),
            (0,0,0,0)
        )
RIGHT_I = (
            (0,0,0,1),
            (0,0,0,1),
            (0,0,0,1),
            (0,0,0,1)
        )
BOTTOM_I = (
            (0,0,0,0),
            (0,0,0,0),
            (0,0,0,0),
            (1,1,1,1)
        )
LEFT_I = (
            (1,0,0,0),
            (1,0,0,0),
            (1,0,0,0),
            (1,0,0,0)
        )
I = (
        TOP_I,
        RIGHT_I,
        BOTTOM_I,
        LEFT_I
    )
TOP_J = (
            (0,1,1,1),
            (0,0,0,1),
            (0,0,0,0),
            (0,0,0,0)
        )
RIGHT_J = (
            (0,0,0,0),
            (0,0,0,1),
            (0,0,0,1),
            (0,0,1,1)
        )
BOTTOM_J = (
            (0,0,0,0),
            (0,0,0,0),
            (1,0,0,0),
            (1,1,1,0)
        )
LEFT_J = (
            (1,1,0,0),
            (1,0,0,0),
            (1,0,0,0),
            (0,0,0,0)
        )
J = (
        TOP_J,
        RIGHT_J,
        BOTTOM_J,
        LEFT_J
    )
TOP_L = (
            (1,1,1,0),
            (1,0,0,0),
            (0,0,0,0),
            (0,0,0,0)
        )
RIGHT_L = (
            (0,0,1,1),
            (0,0,0,1),
            (0,0,0,1),
            (0,0,0,0)
        )
BOTTOM_L = (
            (0,0,0,0),
            (0,0,0,0),
            (0,0,0,1),
            (0,1,1,1)
        )
LEFT_L = (
            (0,0,0,0),
            (1,0,0,0),
            (1,0,0,0),
            (1,1,0,0)
        )
L = (
        TOP_L,
        RIGHT_L,
        BOTTOM_L,
        LEFT_L
    )
TOP_S = (
            (0,0,1,1),
            (0,1,1,0),
            (0,0,0,0),
            (0,0,0,0)
        )
RIGHT_S = (
            (0,0,0,0),
            (0,0,1,0),
            (0,0,1,1),
            (0,0,0,1)
        )
BOTTOM_S = (
            (0,0,0,0),
            (0,0,0,0),
            (0,1,1,0),
            (1,1,0,0)
        )
LEFT_S = (
            (1,0,0,0),
            (1,1,0,0),
            (0,1,0,0),
            (0,0,0,0)
        )
S = (
        TOP_S,
        RIGHT_S,
        BOTTOM_S,
        LEFT_S
    )
TOP_Z = (
            (0,1,1,0),
            (0,0,1,1),
            (0,0,0,0),
            (0,0,0,0)
        )
RIGHT_Z = (
            (0,0,0,0),
            (0,0,0,1),
            (0,0,1,1),
            (0,0,1,0)
        )
BOTTOM_Z = (
            (0,0,0,0),
            (0,0,0,0),
            (1,1,0,0),
            (0,1,1,0)
        )
LEFT_Z = (
            (0,1,0,0),
            (1,1,0,0),
            (1,0,0,0),
            (0,0,0,0)
        )
Z = (
        TOP_Z,
        RIGHT_Z,
        BOTTOM_Z,
        LEFT_Z
    )
TOP_O = (
            (0,0,1,1),
            (0,0,1,1),
            (0,0,0,0),
            (0,0,0,0)
        )
RIGHT_O = (
            (0,0,0,0),
            (0,0,0,0),
            (0,0,1,1),
            (0,0,1,1)
        )
BOTTOM_O = (
            (0,0,0,0),
            (0,0,0,0),
            (1,1,0,0),
            (1,1,0,0)
        )
LEFT_O = (
            (1,1,0,0),
            (1,1,0,0),
            (0,0,0,0),
            (0,0,0,0)
        )
O = (
        TOP_O,
        RIGHT_O,
        BOTTOM_O,
        LEFT_O
    )
TOP_T = (
            (0,0,1,0),
            (0,1,1,1),
            (0,0,0,0),
            (0,0,0,0)
        )
RIGHT_T = (
            (0,0,0,0),
            (0,0,1,0),
            (0,0,1,1),
            (0,0,1,0)
        )
BOTTOM_T = (
            (0,0,0,0),
            (0,0,0,0),
            (1,1,1,0),
            (0,1,0,0)
        )
LEFT_T = (
            (0,1,0,0),
            (1,1,0,0),
            (0,1,0,0),
            (0,0,0,0)
        )
T = (
        TOP_T,
        RIGHT_T,
        BOTTOM_T,
        LEFT_T
    )

def power_on_game_monolithic():
    '''Start the Tetris game loop.

    Initialize the game and handle
    user input until quit command.

    Returns:
        None
    '''
    print("[task] power on")
    # ▼▼▼ init_game() ▼▼▼
    print("[init] initialize")

    # ▼▼▼ init_board() ▼▼▼
    print("[init] init_board")

    # ▼▼▼ create_board() ▼▼▼
    print("[init] create_board")
    global board_result
    global board
    board_result = [
        [0] * BOARD_SIZE_WIDTH
        for _ in range(BOARD_SIZE_HEIGHT)
    ]
    board = [
        [0] * BOARD_SIZE_WIDTH
        for _ in range(BOARD_SIZE_HEIGHT)
    ]
    # ▲▲▲ create_board() ▲▲▲
    # ▲▲▲ init_board() ▲▲▲

    # ▼▼▼ create_blocks() ▼▼▼
    print("[init] create_blocks")
    global block_map_key
    global block_map
    block_map_key = list()
    block_map = {
                    "I": I,
                    "J": J,
                    "L": L,
                    "S": S,
                    "Z": Z,
                    "O": O,
                    "T": T,
                }
    for key in block_map.keys():
        block_map_key.append(key)
    # ▲▲▲ create_blocks() ▲▲▲
    # ▲▲▲ init_game() ▲▲▲

    put_key = ""
    # ▼▼▼ block = get_block() ▼▼▼
    block = (block_map[random.choice(block_map_key)])
    # ▲▲▲ block = get_block() ▲▲▲

    x = 3
    y = 0
    score = 0
    rotation = 0
    new_rotation = 0
    while(put_key != KEY_GAME_FINISH):
    
        if OS_ENVIROMENT == LINUX:
            # ▼▼▼ put_key = getch_for_Linux() ▼▼▼
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)

            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            put_key = ch
            # ▲▲▲ put_key = getch_for_Linux() ▲▲▲
            
        elif OS_ENVIROMENT == WINDOWS:
            if msvcrt.kbhit():
                put_key = msvcrt.getch()
        else:
            put_key = input()   # 標準関数のため展開不要

        # ▼▼▼ rotation = request_operation_rotate(put_key, block, x, y, rotation) ▼▼▼
        print("[req] request_operation_rotate")
        if put_key == KEY_ROTATION_LEFT:

            # ▼▼▼ rotation = request_operation_rotate_left(block, x, y, rotation) ▼▼▼
            print("[req] request_operation_rotate_left")
            new_rotation = rotation - 1
            if new_rotation < 0:
                new_rotation = 3
            
            # ▼▼▼ block_width = get_block_width(block, new_rotation) ▼▼▼
            print("[check] get_block_width")
            width = 0
            for row in block[rotation]:
                for col in range(len(row)):
                    if row[col] == 1:
                        width = max(width, col+1)
            block_width =  width
            # ▲▲▲ block_width = get_block_width(block, new_rotation) ▲▲▲

            # ▼▼▼ block_height = get_block_height(block, new_rotation) ▼▼▼
            print("[check] get_block_height")
            height = 0
            for row in range(len(block[rotation])):
                if 1 in block[rotation][row]:
                    height = row + 1
            block_height =  height
            # ▲▲▲ block_height = get_block_height(block, new_rotation) ▲▲▲

            if x + block_width < 0:
                # print(f"x + block_width:{x + block_width}")
                new_rotation = rotation
            if x + block_width > BOARD_SIZE_WIDTH:
                # print(f"x + block_width:{x + block_width}")
                new_rotation = rotation
            if y + block_height < 0:
                # print(f"x + block_width:{x + block_height}")
                new_rotation = rotation
            if y + block_height > BOARD_SIZE_HEIGHT:
                # print(f"x + block_width:{x + block_height}")
                new_rotation = rotation
            # ▲▲▲ rotation = request_operation_rotate_left(block, x, y, rotation) ▲▲▲

        if put_key == KEY_ROTATION_RIGHT:
            # ▼▼▼ rotation = request_operation_rotate_right(block, x, y, rotation) ▼▼▼
            print("[req] request_operation_rotate_right")
            new_rotation = rotation + 1
            new_rotation = new_rotation % 4

            # ▼▼▼ block_width = get_block_width(block, new_rotation) ▼▼▼
            print("[check] get_block_width")
            width = 0
            for row in block[rotation]:
                for col in range(len(row)):
                    if row[col] == 1:
                        width = max(width, col+1)
            block_width =  width
            # ▲▲▲ block_width = get_block_width(block, new_rotation) ▲▲▲

            # ▼▼▼ block_height = get_block_height(block, new_rotation) ▼▼▼
            print("[check] get_block_height")
            height = 0
            for row in range(len(block[rotation])):
                if 1 in block[rotation][row]:
                    height = row + 1
            block_height =  height
            # ▲▲▲ block_height = get_block_height(block, new_rotation) ▲▲▲
            if x + block_width< 0:
                # print(f"x + block_width:{x + block_width}")
                new_rotation = rotation
            if x + block_width >= BOARD_SIZE_WIDTH:
                # print(f"x + block_width:{x + block_width}")
                new_rotation = rotation
            if y + block_height< 0:
                # print(f"x + block_width:{x + block_height}")
                new_rotation = rotation
            if y + block_height >= BOARD_SIZE_HEIGHT:
                # print(f"x + block_width:{x + block_height}")
                new_rotation = rotation

            # ▲▲▲ rotation = request_operation_rotate_right(block, x, y, rotation) ▲▲▲

        rotation =  new_rotation
        # ▲▲▲ rotation = request_operation_rotate(put_key, block, x, y, rotation) ▲▲▲

        # ▼▼▼ next_x, next_y = get_next_position(put_key, x, y) ▼▼▼
        print("[req] get_next_position")

        next_x = x
        next_y = y
        if put_key == KEY_RIGHT:
            next_x += 1
        elif put_key == KEY_LEFT:
            next_x -= 1
        elif put_key == KEY_DROP:
            next_y += 1
        else:
            # Do Nothing
            pass
        # ▲▲▲ next_x, next_y = get_next_position(put_key, x, y) ▲▲▲

        # ▼▼▼ if is_invalid_position(block, c, next_y, rotation): ▼▼▼
        print("[check] is_invalid_position")
        is_invalid_position_is_invalid = False

        # ▼▼▼ is_invalid_move = is_out_of_board(block, x, y, rotation) ▼▼▼
        print("[check] is_out_of_board")
        is_out_of_board_is_invalid = False

        # ▼▼▼ block_width = get_block_width(block, new_rotation) ▼▼▼
        print("[check] get_block_width")
        width = 0
        for row in block[rotation]:
            for col in range(len(row)):
                if row[col] == 1:
                    width = max(width, col+1)
        block_width =  width
        # ▲▲▲ block_width = get_block_width(block, new_rotation) ▲▲▲

        # ▼▼▼ block_height = get_block_height(block, new_rotation) ▼▼▼
        print("[check] get_block_height")
        height = 0
        for row in range(len(block[rotation])):
            if 1 in block[rotation][row]:
                height = row + 1
        block_height =  height
        # ▲▲▲ block_height = get_block_height(block, new_rotation) ▲▲▲

        if next_x < 0:
            is_out_of_board_is_invalid = True
        if next_y < 0:
            is_out_of_board_is_invalid = True
        if next_x > BOARD_SIZE_WIDTH-block_width:
            is_out_of_board_is_invalid = True
        if next_y > BOARD_SIZE_HEIGHT-block_height:
            is_out_of_board_is_invalid = True
        is_invalid_move =  is_out_of_board_is_invalid
        # ▲▲▲ is_invalid_move = is_out_of_board(block, x, y, rotation) ▲▲▲

        # ▼▼▼ is_invalid_rotate = check_operation_rotate() ▼▼▼
        print("[check] check_operation_rotate")
        is_invalid_rotate =  False
        # ▲▲▲ is_invalid_rotate = check_operation_rotate() ▲▲▲
        if is_invalid_move or is_invalid_rotate:
            is_invalid_position_is_invalid = True
        # ▲▲▲ if is_invalid_position(block, next_x, next_y, rotation): ▲▲▲
        if is_invalid_position_is_invalid:
            next_x = x
            next_y = y

        # 衝突検知
        # ▼▼▼ if check_collision_detection(block, next_x, next_y, rotation): ▼▼▼
        print("[check] check_collision_detection")

        # ▼▼▼ block_width = get_block_width(block, new_rotation) ▼▼▼
        print("[check] get_block_width")
        width = 0
        for row in block[rotation]:
            for col in range(len(row)):
                if row[col] == 1:
                    width = max(width, col+1)
        block_width =  width
        # ▲▲▲ block_width = get_block_width(block, new_rotation) ▲▲▲

        # ▼▼▼ block_height = get_block_height(block, new_rotation) ▼▼▼
        print("[check] get_block_height")
        height = 0
        for row in range(len(block[rotation])):
            if 1 in block[rotation][row]:
                height = row + 1
        block_height =  height
        # ▲▲▲ block_height = get_block_height(block, new_rotation) ▲▲▲

        check_collision_detection_result = False
        for r in range(len(block[rotation])):
            for c in range(len(block[rotation][r])):
                # 衝突検知(床)
                if next_y >= BOARD_SIZE_HEIGHT - block_height:
                    # print(f"next_y:{next_y}")
                    check_collision_detection_result = True
                    break
                
                # next(blockなし)
                if block[rotation][r][c] != 1:
                    continue
                
                # 衝突検知(board block)
                if board_result[next_y+r][next_x+c] == 1:
                    # print(f"next_y+r:{next_y+r}")
                    # print(f"next_x+c:{next_x+c}")
                    check_collision_detection_result = True
                    break
                
                # 衝突検知(next board block)
                if board_result[next_y+r+1][next_x+c] == 1:
                    # print(f"next_y+r+1:{next_y+r+1}")
                    # print(f"next_x+c:{next_x+c}")
                    check_collision_detection_result = True
                    break
            if check_collision_detection_result:
                break
        # ▲▲▲ if check_collision_detection(block, next_x, next_y, rotation): ▲▲▲

        if check_collision_detection_result:
            # ▼▼▼ fix_block(block, next_x, next_y, rotation) # update board result▼▼▼
            for r in range(len(block[rotation])):
                for c in range(len(block[rotation][r])):
                    if block[rotation][r][c] == 1:
                        board_result[next_y+r][next_x+c] = 1
                        # print("check", y+r, x+c)
            # ▲▲▲ fix_block(block, next_x, next_y, rotation) # update board result▲▲▲

            # game over
            is_game_over_result = False

            # ▼▼▼ if is_game_over(put_key) == True: ▼▼▼
            if put_key == KEY_DROP:
                next_y = 1
            else:
                next_y = 0
            for c in range(len(board_result[next_y])):
                if board_result[next_y][c] == 1:
                    is_game_over_result = True
                    break
            # ▲▲▲ if is_game_over(put_key) == True: ▲▲▲

            if is_game_over_result:
                print("game over!")
                break

            # bingo
            # ▼▼▼ bingo_lines = get_bingo_lines() ▼▼▼
            delete_rows = []
            for r in range(len(board_result)):
                for c in range(len(board_result[r])):
                    if board_result[r][c] != 1:
                        break
                    if c >= BOARD_SIZE_WIDTH-1:
                        delete_rows.append(r)
                        print("bingo!!")
            bingo_lines =  delete_rows
            # ▲▲▲ bingo_lines = get_bingo_lines() ▲▲▲
            
            score += len(bingo_lines)

            # ▼▼▼ clear_bingo_lines() ▼▼▼
            # global board_result
            new_board = []

            for row in board_result:
                if row.count(1) < BOARD_SIZE_WIDTH:
                    new_board.append(row)

            while len(new_board) < BOARD_SIZE_HEIGHT:
                new_board.insert(
                    0,
                    [0] * BOARD_SIZE_WIDTH
                )
            board_result = new_board
            # ▲▲▲ clear_bingo_lines() ▲▲▲
            
            # ▼▼▼ block = get_block() ▼▼▼
            block = (block_map[random.choice(block_map_key)])
            # ▲▲▲ block = get_block() ▲▲▲

            # print(block)
            x = 3
            y = 0
            rotation = 0
        else:
            x = next_x
            y = next_y

        # ▼▼▼ update_view(block, x, y, rotation) ▼▼▼
        print("[view] update_view")

        # view
        # global board

        # ▼▼▼ load_board_result()                   # おばけ(残像)を消す ▼▼▼
        print("[init] load_board_result")
        # global board
        board = []

        for row in board_result:
            board.append(row[:])
        # print(board_result)
        # print(id(board[0]))
        # print(id(board_result[0]))
        # ▲▲▲ load_board_result()                   # おばけ(残像)を消す ▲▲▲

        for r in range(len(block[rotation])):
            for c in range(len(block[rotation][r])):
                if block[rotation][r][c] == 1:
                    board[y+r][x+c] = 1
                    # print(f"r+y: {r+y}")
                    # print(f"c+x: {c+x}")

        # ▼▼▼ draw_board(board) ▼▼▼
        print("[proc] draw_board")
        for row in board:
            line = ""

            for cell in row:
                if cell == 0:
                    line += "□"
                else:
                    line += "■"
            print(line)
        # ▲▲▲ draw_board(board) ▲▲▲

        # ▲▲▲ update_view(block, x, y, rotation) ▲▲▲
        
    print(f"score : {score * 100}")




# def update_view(block, x, y, rotation):
#     '''Draw block on the board.

#     Clear the previous frame and redraw
#     the current block position.

#     Args:
#         block (tuple):
#             Tetromino shape data.
#         x (int):
#             X-coordinate on the board.
#         y (int):
#             Y-coordinate on the board.
#     '''
#     print("[view] update_view")

#     # view
#     global board
#     load_board_result()                   # おばけ(残像)を消す
#     for r in range(len(block[rotation])):
#         for c in range(len(block[rotation][r])):
#             if block[rotation][r][c] == 1:
#                 board[y+r][x+c] = 1
#                 # print(f"r+y: {r+y}")
#                 # print(f"c+x: {c+x}")
#     draw_board(board)

# '''user input header
# user input functions

# Todo:
#     * rotate
# '''
# def request_operation_rotate(put_key, block, x, y, rotation):
#     '''Handle user input for block movement and rotation.

#     Args:
#         put_key (str):
#             User keyboard input.
#         block (tuple):
#             Current tetromino shape.
#         x (int):
#             Current x-coordinate on the board.
#         y (int):
#             Current y-coordinate on the board.

#     Returns:
#         tuple:
#             Updated block, x-coordinate, and y-coordinate.
#     '''
#     print("[req] request_operation_rotate")
#     if put_key == KEY_ROTATION_LEFT:
#         rotation = request_operation_rotate_left(block, x, y, rotation)
#     if put_key == KEY_ROTATION_RIGHT:
#         rotation = request_operation_rotate_right(block, x, y, rotation)
#     return rotation

# def get_next_position(put_key, x, y):
#     '''Handle user input for block movement.

#     Args:
#         put_key (str):
#             User keyboard input.
#         x (int):
#             Current x-coordinate on the board.
#         y (int):
#             Current y-coordinate on the board.

#     Returns:
#         tuple:
#             Updated block, next_x-coordinate, and next_y-coordinate.
#     '''
#     print("[req] get_next_position")

#     next_x = x
#     next_y = y
#     if put_key == KEY_RIGHT:
#         next_x += 1
#     elif put_key == KEY_LEFT:
#         next_x -= 1
#     elif put_key == KEY_DROP:
#         next_y += 1
#     else:
#         # Do Nothing
#         pass

#     return next_x, next_y

# def request_operation_rotate_left(block, x, y, rotation):
#     '''Rotate block to the left.

#     Args:
#         block (tuple):
#             Current tetromino shape.
#         x (int):
#             Current x-coordinate.
#         y (int):
#             Current y-coordinate.

#     Returns:
#         tuple:
#             Updated block, x-coordinate, and y-coordinate.
#     '''
#     print("[req] request_operation_rotate_left")
#     new_rotation = rotation - 1
#     if new_rotation < 0:
#         new_rotation = 3
    
#     block_width = get_block_width(block, new_rotation)
#     block_height = get_block_height(block, new_rotation)
#     if x + block_width < 0:
#         # print(f"x + block_width:{x + block_width}")
#         new_rotation = rotation
#     if x + block_width > BOARD_SIZE_WIDTH:
#         # print(f"x + block_width:{x + block_width}")
#         new_rotation = rotation
#     if y + block_height < 0:
#         # print(f"x + block_width:{x + block_height}")
#         new_rotation = rotation
#     if y + block_height > BOARD_SIZE_HEIGHT:
#         # print(f"x + block_width:{x + block_height}")
#         new_rotation = rotation

#     return new_rotation

# def request_operation_rotate_right(block, x, y, rotation):
#     '''Rotate block to the right.

#     Args:
#         block (tuple):
#             Current tetromino shape.
#         x (int):
#             Current x-coordinate.
#         y (int):
#             Current y-coordinate.

#     Returns:
#         tuple:
#             Updated block, x-coordinate, and y-coordinate.
#     '''
#     print("[req] request_operation_rotate_right")
#     new_rotation = rotation + 1
#     new_rotation = new_rotation % 4

#     block_width = get_block_width(block, new_rotation)
#     block_height = get_block_height(block, new_rotation)
#     if x + block_width< 0:
#         # print(f"x + block_width:{x + block_width}")
#         new_rotation = rotation
#     if x + block_width >= BOARD_SIZE_WIDTH:
#         # print(f"x + block_width:{x + block_width}")
#         new_rotation = rotation
#     if y + block_height< 0:
#         # print(f"x + block_width:{x + block_height}")
#         new_rotation = rotation
#     if y + block_height >= BOARD_SIZE_HEIGHT:
#         # print(f"x + block_width:{x + block_height}")
#         new_rotation = rotation

#     return new_rotation

# '''update check header
# update check functions

# Todo:
#     * rotate
# '''
# def is_invalid_position(block, x, y, rotation):
#     '''Validate block movement and rotation.

#     Correct coordinates to prevent
#     movement outside the board.

#     Args:
#         block (tuple):
#             Current tetromino shape.
#         x (int):
#             Updated x-coordinate.
#         y (int):
#             Updated y-coordinate.

#     Returns:
#         tuple:
#             Corrected x-coordinate
#             and y-coordinate.
#     '''
#     print("[check] is_invalid_position")
#     is_invalid = False
#     is_invalid_move = is_out_of_board(block, x, y, rotation)
#     is_invalid_rotate = check_operation_rotate()
#     if is_invalid_move or is_invalid_rotate:
#         is_invalid = True
#     return is_invalid

# def is_out_of_board(block, x, y, rotation):
#     '''Check movable range of the block.

#     Prevent block movement outside
#     the board boundary.

#     Args:
#         block (tuple):
#             Current tetromino shape.
#         x (int):
#             X-coordinate.
#         y (int):
#             Y-coordinate.

#     Returns:
#         (bool)
#             True  : Under or Over
#             False : Within the specified range
#     '''
#     print("[check] is_out_of_board")
#     is_invalid = False
#     block_width = get_block_width(block, rotation)
#     block_height = get_block_height(block, rotation)
#     if x < 0:
#         is_invalid = True
#     if y < 0:
#         is_invalid = True
#     if x > BOARD_SIZE_WIDTH-block_width:
#         is_invalid = True
#     if y > BOARD_SIZE_HEIGHT-block_height:
#         is_invalid = True
#     return is_invalid

# def check_collision_detection(block, next_x, next_y, rotation):
#     '''Check if there was a collision with a block.

#     Detecting Block Collisions.

#     Args:
#         block (tuple):
#             Current tetromino shape.
#         x (int):
#             X-coordinate.
#         y (int):
#             Y-coordinate.

#     Returns:
#         tuple:
#             Corrected x-coordinate
#             and y-coordinate.
#     '''
#     print("[check] check_collision_detection")
#     block_width = get_block_width(block, rotation)
#     block_height = get_block_height(block, rotation)
#     for r in range(len(block[rotation])):
#         for c in range(len(block[rotation][r])):
#             # 衝突検知(床)
#             if next_y >= BOARD_SIZE_HEIGHT - block_height:
#                 # print(f"next_y:{next_y}")
#                 return True
            
#             # next(blockなし)
#             if block[rotation][r][c] != 1:
#                 continue
            
#             # 衝突検知(board block)
#             if board_result[next_y+r][next_x+c] == 1:
#                 # print(f"next_y+r:{next_y+r}")
#                 # print(f"next_x+c:{next_x+c}")
#                 return True
            
#             # 衝突検知(next board block)
#             if board_result[next_y+r+1][next_x+c] == 1:
#                 # print(f"next_y+r+1:{next_y+r+1}")
#                 # print(f"next_x+c:{next_x+c}")
#                 return True
            
#     return False

# def get_block_width(block, rotation):
#     '''Get effective block width.

#     Calculate the actual width of a block
#     excluding trailing empty cells.

#     Args:
#         block (tuple):
#             Tetromino shape data.

#     Returns:
#         int:
#             Effective width of the block.
#     '''
#     print("[check] get_block_width")
#     width = 0
#     for row in block[rotation]:
#         for col in range(len(row)):
#             if row[col] == 1:
#                 width = max(width, col+1)
#     return width

# def get_block_height(block, rotation):
#     '''Get effective block height.

#     Calculate the actual height of a block
#     excluding trailing empty cells.

#     Args:
#         block (tuple):
#             Tetromino shape data.

#     Returns:
#         int:
#             Effective height of the block.
#     '''
#     print("[check] get_block_height")
#     height = 0
#     for row in range(len(block[rotation])):
#         if 1 in block[rotation][row]:
#             height = row + 1

#     return height

# def check_operation_rotate():
#     '''Check block rotation validity.

#     Validate whether rotation is
#     allowed in the current position.

#     Returns:
#         None
#     '''
#     print("[check] check_operation_rotate")
#     return False



# def load_board_result():
#     '''Restore the drawing board.

#         Create a working board from
#         the current board_result state.

#         Returns:
#             None
#     '''
#     print("[init] load_board_result")
#     global board
#     board = []

#     for row in board_result:
#         board.append(row[:])
#     # print(board_result)
#     # print(id(board[0]))
#     # print(id(board_result[0]))

# def draw_board(board):
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

# def fix_block(block, x, y, rotation):
#     '''Fix the block on the board.

#         Store the current block into
#         board_result as a fixed block.

#         Args:
#             block (tuple):
#                 Current tetromino shape.
#             x (int):
#                 X-coordinate.
#             y (int):
#                 Y-coordinate.

#         Returns:
#             None
#     '''
#     global board_result
#     for r in range(len(block[rotation])):
#         for c in range(len(block[rotation][r])):
#             if block[rotation][r][c] == 1:
#                 board_result[y+r][x+c] = 1
#                 # print("check", y+r, x+c)

# def get_bingo_lines():
#     delete_rows = []
#     for r in range(len(board_result)):
#         for c in range(len(board_result[r])):
#             if board_result[r][c] != 1:
#                 break
#             if c >= BOARD_SIZE_WIDTH-1:
#                 delete_rows.append(r)
#                 print("bingo!!")
#     return delete_rows

# def clear_bingo_lines():
#     global board_result
#     new_board = []

#     for row in board_result:
#         if row.count(1) < BOARD_SIZE_WIDTH:
#             new_board.append(row)

#     while len(new_board) < BOARD_SIZE_HEIGHT:
#         new_board.insert(
#             0,
#             [0] * BOARD_SIZE_WIDTH
#         )
#     board_result = new_board

# def is_game_over(put_key):
#     if put_key == KEY_DROP:
#         next_y = 1
#     else:
#         next_y = 0
#     for c in range(len(board_result[next_y])):
#         if board_result[next_y][c] == 1:
#             return True
#     return False     


if __name__ == "__main__":
    power_on_game_monolithic()
    print("[task] power off")
