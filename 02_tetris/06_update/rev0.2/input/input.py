from settings import(
    OS_ENVIROMENT,
    LINUX,
    WINDOWS,
    KEY_DROP,
    KEY_LEFT,
    KEY_RIGHT,
    KEY_ROTATION_LEFT,
    KEY_ROTATION_RIGHT,
    BOARD_SIZE_WIDTH,
    BOARD_SIZE_HEIGHT,
    KEY_HARD_DROP
)
from block.block import(
    get_block_width,
    get_block_height
)
from collision.collision import(
    execute_hard_drop,
    check_move_collision
)

_put_key = None

if OS_ENVIROMENT == LINUX:
    import sys
    import termios
    import tty
    import select
    _old_settings = None
elif OS_ENVIROMENT == WINDOWS:
    import msvcrt
else:
    # Do Nothing
    pass

def init_input():
    """プログラム開始時に1回呼び出してターミナルを入力監視モードにする"""
    global _old_settings, _put_key
    _put_key = None
    if OS_ENVIROMENT == LINUX:
        fd = sys.stdin.fileno()
        _old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)  # Ctrl+Cで終了可能なcbreakモード

def restore_input():
    """プログラム終了時にターミナル設定を元に戻す"""
    global _old_settings
    if OS_ENVIROMENT == LINUX and _old_settings:
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, _old_settings)

def request_operation_rotate(put_key, block, x, y, rotation):
    '''Handle user input for block movement and rotation.

    Args:
        put_key (str):
            User keyboard input.
        block (tuple):
            Current tetromino shape.
        x (int):
            Current x-coordinate on the board.
        y (int):
            Current y-coordinate on the board.

    Returns:
        tuple:
            Updated block, x-coordinate, and y-coordinate.
    '''
    # print("[req] request_operation_rotate")
    if put_key == KEY_ROTATION_LEFT:
        next_rotation = request_operation_rotate_left(block, x, y, rotation)
    elif put_key == KEY_ROTATION_RIGHT:
        next_rotation = request_operation_rotate_right(block, x, y, rotation)
    else:
        next_rotation = rotation

    # # 回転後の状態を検証
    # if check_move_collision(block, x, y, next_rotation):
    #     # 回転できないので、元の回転状態を維持
    #     next_rotation = rotation
    return next_rotation

def get_next_position(put_key, block, x, y, rotation):
    '''Handle user input for block movement.

    Args:
        put_key (str):
            User keyboard input.
        x (int):
            Current x-coordinate on the board.
        y (int):
            Current y-coordinate on the board.

    Returns:
        tuple:
            Updated block, next_x-coordinate, and next_y-coordinate.
    '''
    # print("[req] get_next_position")
    next_x = x
    next_y = y
    if put_key == KEY_RIGHT:
        next_x += 1
    elif put_key == KEY_LEFT:
        next_x -= 1
    elif put_key == KEY_DROP:
        next_y += 1
    elif put_key == KEY_HARD_DROP:
        next_y = execute_hard_drop(block, x, y, rotation)
    else:
        # Do Nothing
        pass

    return next_x, next_y

def request_operation_rotate_left(block, x, y, rotation):
    '''Rotate block to the left.

    Args:
        block (tuple):
            Current tetromino shape.
        x (int):
            Current x-coordinate.
        y (int):
            Current y-coordinate.

    Returns:
        tuple:
            Updated block, x-coordinate, and y-coordinate.
    '''
    # print("[req] request_operation_rotate_left")
    new_rotation = rotation - 1
    if new_rotation < 0:
        new_rotation = 3

    # block_width = get_block_width(block, new_rotation)
    # block_height = get_block_height(block, new_rotation)
    # if x + block_width < 0:
    #     # print(f"x + block_width:{x + block_width}")
    #     new_rotation = rotation
    # if x + block_width > BOARD_SIZE_WIDTH:
    #     # print(f"x + block_width:{x + block_width}")
    #     new_rotation = rotation
    # if y + block_height < 0:
    #     # print(f"x + block_width:{x + block_height}")
    #     new_rotation = rotation
    # if y + block_height > BOARD_SIZE_HEIGHT:
    #     # print(f"x + block_width:{x + block_height}")
    #     new_rotation = rotation

    return new_rotation

def request_operation_rotate_right(block, x, y, rotation):
    '''Rotate block to the right.

    Args:
        block (tuple):
            Current tetromino shape.
        x (int):
            Current x-coordinate.
        y (int):
            Current y-coordinate.

    Returns:
        tuple:
            Updated block, x-coordinate, and y-coordinate.
    '''
    # print("[req] request_operation_rotate_right")
    new_rotation = rotation + 1
    new_rotation = new_rotation % 4

    # block_width = get_block_width(block, new_rotation)
    # block_height = get_block_height(block, new_rotation)
    # if x + block_width< 0:
    #     # print(f"x + block_width:{x + block_width}")
    #     new_rotation = rotation
    # if x + block_width >= BOARD_SIZE_WIDTH:
    #     # print(f"x + block_width:{x + block_width}")
    #     new_rotation = rotation
    # if y + block_height< 0:
    #     # print(f"x + block_width:{x + block_height}")
    #     new_rotation = rotation
    # if y + block_height >= BOARD_SIZE_HEIGHT:
    #     # print(f"x + block_width:{x + block_height}")
    #     new_rotation = rotation

    return new_rotation

def get_key_non_blocking():
    """キー入力をノンブロッキングで取得する（タイムアウト0）"""
    if OS_ENVIROMENT == LINUX:
        rlist, _, _ = select.select([sys.stdin], [], [], 0)
        if rlist:
            ch = sys.stdin.read(1)
            # 矢印キー（エスケープシーケンス）の処理
            if ch == '\x1b':
                rlist_sub, _, _ = select.select([sys.stdin], [], [], 0)
                if rlist_sub:
                    extra = sys.stdin.read(2)
                    return f"arrow_{extra}"
            return ch
    elif OS_ENVIROMENT == WINDOWS:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            try:
                return key.decode('utf-8')
            except UnicodeDecodeError:
                return str(key)
    return None

def get_putkey():
    global _put_key
    result = _put_key
    _put_key = None
    return result

def input_putkey():
    """毎ミリ秒（メインループ）で呼び出す"""
    global _put_key
    key = get_key_non_blocking()
    if key:
        _put_key = key
