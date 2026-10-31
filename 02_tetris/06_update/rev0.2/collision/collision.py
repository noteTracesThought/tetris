from settings import(
    BOARD_SIZE_WIDTH,
    BOARD_SIZE_HEIGHT
)
from board.board import get_board_result

from block.block import(
    check_operation_rotate
)

'''update check header
update check functions

Todo:
    * rotate
'''
def is_invalid_position(block, x, y, rotation):
    '''Validate block movement and rotation.

    Correct coordinates to prevent
    movement outside the board.

    Args:
        block (tuple):
            Current tetromino shape.
        x (int):
            Updated x-coordinate.
        y (int):
            Updated y-coordinate.

    Returns:
        tuple:
            Corrected x-coordinate
            and y-coordinate.
    '''
    # print("[check] is_invalid_position")
    is_invalid = False
    is_invalid_move = is_out_of_board(block, x, y, rotation)
    is_invalid_rotate = check_operation_rotate()
    if is_invalid_move or is_invalid_rotate:
        is_invalid = True
    return is_invalid

def is_out_of_board(block, x, y, rotation):
    '''Check movable range of the block.

    Prevent block movement outside
    the board boundary.

    Args:
        block (tuple):
            Current tetromino shape.
        x (int):
            X-coordinate.
        y (int):
            Y-coordinate.

    Returns:
        (bool)
            True  : Under or Over
            False : Within the specified range
    '''
    # print("[check] is_out_of_board")
    if rotation < 0 or rotation >= len(block):
        return True

    for r, row in enumerate(block[rotation]):
        for c, cell in enumerate(row):
            if cell != 1:
                continue
            board_x = x + c
            board_y = y + r
            if not (0 <= board_x < BOARD_SIZE_WIDTH and 0 <= board_y < BOARD_SIZE_HEIGHT):
                return True
    return False

def check_fall_collision(block, next_x, next_y, rotation):
    '''Check if there was a collision with a block.

    Detecting Block Collisions.

    Args:
        block (tuple):
            Current tetromino shape.
        x (int):
            X-coordinate.
        y (int):
            Y-coordinate.

    Returns:
        tuple:
            Corrected x-coordinate
            and y-coordinate.
    '''
    # print("[check] check_collision_detection")
    if check_move_collision(block, next_x, next_y, rotation):
        return True
    return check_move_collision(block, next_x, next_y + 1, rotation)

def check_move_collision(block, next_x, next_y, rotation):
    '''Check if there was a collision with a block.

    Detecting Block Collisions.

    Args:
        block (tuple):
            Current tetromino shape.
        x (int):
            X-coordinate.
        y (int):
            Y-coordinate.

    Returns:
        tuple:
            Corrected x-coordinate
            and y-coordinate.
    '''
    # print("[check] check_collision_detection")
    if is_out_of_board(block, next_x, next_y, rotation):
        return True

    current_block = block[rotation]
    board_result = get_board_result()
    for r, row in enumerate(current_block):
        for c, cell in enumerate(row):
            if cell == 1 and board_result[next_y + r][next_x + c] == 1:
                return True
    return False

WALL_KICK_X = (0, -1, 1, -2, 2, -3, 3)
def adjust_pos(block, x, y, rotation):
    for offset_x in WALL_KICK_X:
        next_x = x + offset_x

        if not check_move_collision(block, next_x, y, rotation):
            return next_x, y, rotation

    return x, y, rotation

def execute_hard_drop(block, x, y, rotation):
    '''ハードドロップを実行する'''
    current_y = y
    next_y = y

    while True:
        # 仮想的に1段下の位置（Position）を計算して next にセットするだけ
        next_y += 1

        # その1段下（next）で衝突するかチェック
        if check_fall_collision(block, x, next_y, rotation):
            # ぶつかるなら、今の current（衝突する直前の安全な位置）が最終位置なので終了
            break

        # ぶつからなければ、現在位置(current)を1段下に進めて次のループへ
        current_y = next_y
    next_y = current_y

    return next_y
