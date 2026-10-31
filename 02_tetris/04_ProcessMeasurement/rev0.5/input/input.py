import domain.constants.playboard    as brddc
from domain.models.entities.tetromino import Tetromino
from domain.models.valueobject.position import MovePosition
# ▼▼▼ ハードドロップ機能追加 ▼▼▼
from collision.collision import Collision
# ▲▲▲ ハードドロップ機能追加 ▲▲▲

# ▼▼▼ ハードドロップ機能追加 ▼▼▼
from settings import OS_ENVIROMENT, LINUX, WINDOWS, KEY_GAME_FINISH, KEY_DROP, KEY_LEFT, KEY_RIGHT, KEY_ROTATION_LEFT, KEY_ROTATION_RIGHT, KEY_HARD_DROP
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

# ▼▼▼ ハードドロップ機能追加 ▼▼▼
    def __init__(self, tetromino:Tetromino, blocks_map, blocks, collision:Collision):
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
        self.tetromino = tetromino
        self.blocks_map = blocks_map
        self.blocks = blocks
# ▼▼▼ ハードドロップ機能追加 ▼▼▼
        self.collision = collision
# ▲▲▲ ハードドロップ機能追加 ▲▲▲

    def getch_for_Linux(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        return ch

    # def request_operation_rotate(self, put_key, block):
    def request_operation_rotate(self, put_key):
        '''Handle user input for block movement and rotation.

        Args:
            put_key (str):
                User keyboard input.
            block (tuple):
                Current tetromino shape.

        Returns:
            None
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[req] request_operation_rotate")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        if put_key == KEY_ROTATION_LEFT:
            # self.pos.rotation = Rotation(self.request_operation_rotate_left(block))
            self.tetromino.rotate_left()
        if put_key == KEY_ROTATION_RIGHT:
            # self.pos.rotation = Rotation(self.request_operation_rotate_right(block))
            self.tetromino.rotate_right()

    def get_next_position(self, put_key):
        '''Handle user input for block movement.

        Args:
            put_key (str):
                User keyboard input.

        Returns:
            None

        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[req] get_next_position")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        # self.pos.next.x = self.pos.current.x
        # self.pos.next.y = self.pos.current.y
        pos = self.tetromino.get_position()

        # 移動先（next）の計算を Position のメソッドに任せる
        try:
            if put_key == KEY_RIGHT:
                # next_x += 1
                next_pos = pos.current.move_right()
            elif put_key == KEY_LEFT:
                # next_x -= 1
                next_pos = pos.current.move_left()
            elif put_key == KEY_DROP:
                # next_y += 1
                next_pos = pos.current.move_down()
# ▼▼▼ ハードドロップ機能追加 ▼▼▼
            elif put_key == KEY_HARD_DROP:
                block = self.tetromino.get_tetromino()
                next_pos = self.collision.execute_hard_drop(block)
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
                
            else:
                # # Do Nothing
                # pass
                next_pos = pos.current

            return MovePosition(current=pos.current, next=next_pos)

        except ValueError:
            # 盤面外などで PosX/PosY の生成に失敗した場合は位置を変更しない
            return MovePosition(current=pos.current, next=pos.current)

    # def request_operation_rotate_left(self, block):
    def request_operation_rotate_left(self):
        '''Rotate block to the left.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            tuple:
                Updated block, x-coordinate, and y-coordinate.
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[req] request_operation_rotate_left")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        new_rotation = self.tetromino.get_rotation() - 1
        if new_rotation < 0:
            new_rotation = 3
        
        # block_width = self.blocks.get_block_width(block, new_rotation)
        # block_height = self.blocks.get_block_height(block, new_rotation)
        block_width = self.tetromino.width()
        block_height = self.tetromino.height()

        pos = self.tetromino.get_position()
        rotation = self.tetromino.get_rotation()
        if pos.current.x.value + block_width < 0:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = rotation
        if pos.current.x.value + block_width > brddc.PlayBoardSize.WIDTH:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = rotation
        if pos.current.y.value + block_height < 0:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = rotation
        if pos.current.y.value + block_height > brddc.PlayBoardSize.HEIGHT:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = rotation

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
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[req] request_operation_rotate_right")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        new_rotation = self.tetromino.get_rotation()
        new_rotation = new_rotation % 4

        # block_width = self.blocks.get_block_width(block, new_rotation)
        # block_height = self.blocks.get_block_height(block, new_rotation)
        block_width = self.tetromino.width()
        block_height = self.tetromino.height()

        pos = self.tetromino.get_position()
        rotation = self.tetromino.get_rotation()
        if pos.current.x.value + block_width< 0:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = rotation
        if pos.current.x.value + block_width >= brddc.PlayBoardSize.WIDTH:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = rotation
        if pos.current.y.value + block_height< 0:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = rotation
        if pos.current.y.value + block_height >= brddc.PlayBoardSize.HEIGHT:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = rotation

        return new_rotation
