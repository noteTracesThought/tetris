# ▼▼▼ ハードドロップ機能追加 ▼▼▼
from settings import OS_ENVIROMENT, \
                     LINUX, \
                     WINDOWS, \
                     KEY_DROP, \
                     KEY_LEFT, \
                     KEY_RIGHT, \
                     KEY_ROTATION_LEFT, \
                     KEY_ROTATION_RIGHT, \
                     BOARD_SIZE_WIDTH, \
                     BOARD_SIZE_HEIGHT, \
                     KEY_HARD_DROP
# ▲▲▲ ハードドロップ機能追加 ▲▲▲

from block.block import Blocks
# ▼▼▼ ハードドロップ機能追加 ▼▼▼
from collision.collision import Collision
# ▲▲▲ ハードドロップ機能追加 ▲▲▲

if OS_ENVIROMENT == LINUX:
    import sys
    import termios
    import tty
elif OS_ENVIROMENT == WINDOWS:
    import msvcrt
else:
    # Do Nothing
    pass

class Input():
    '''user input header
    user input functions

    Todo:
        * rotate
    '''

    def getch_for_Linux():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        return ch

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
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[req] request_operation_rotate")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        if put_key == KEY_ROTATION_LEFT:
            rotation = Input.request_operation_rotate_left(block, x, y, rotation)
        if put_key == KEY_ROTATION_RIGHT:
            rotation = Input.request_operation_rotate_right(block, x, y, rotation)
        return rotation

# ▼▼▼ ハードドロップ機能追加 ▼▼▼
    def get_next_position(put_key, block, x, y, rotation):
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
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
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[req] get_next_position")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲

        next_x = x
        next_y = y
        if put_key == KEY_RIGHT:
            next_x += 1
        elif put_key == KEY_LEFT:
            next_x -= 1
        elif put_key == KEY_DROP:
            next_y += 1
# ▼▼▼ ハードドロップ機能追加 ▼▼▼
        elif put_key == KEY_HARD_DROP:
            next_y = Collision.execute_hard_drop(block, x, y, rotation)
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
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
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[req] request_operation_rotate_left")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        new_rotation = rotation - 1
        if new_rotation < 0:
            new_rotation = 3
        
        block_width = Blocks.get_block_width(block, new_rotation)
        block_height = Blocks.get_block_height(block, new_rotation)
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
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[req] request_operation_rotate_right")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        new_rotation = rotation + 1
        new_rotation = new_rotation % 4

        block_width = Blocks.get_block_width(block, new_rotation)
        block_height = Blocks.get_block_height(block, new_rotation)
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

        return new_rotation
