import board.playboard    as brddc

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
    import select
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
    def __init__(self, pos, blocks_map, blocks, collision:Collision):
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
        self.pos = pos
        self.blocks_map = blocks_map
        self.blocks = blocks
# ▼▼▼ ハードドロップ機能追加 ▼▼▼
        self.collision = collision
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
        self.put_key = ''

    def getch_for_Linux(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            # ch = sys.stdin.read(1)
            # 1. 入力があるかをチェック（タイムアウトを0に設定して即座に判定）
            # [sys.stdin] を監視し、読み込み可能なら rlist に値が入る
            rlist, _, _ = select.select([sys.stdin], [], [], 0)

            if rlist:
                ch = sys.stdin.read(1)  # 入力があれば読み込む
            else:
                ch = None  # 入力がなければ None を返してスルー
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

        return ch

    def request_operation_rotate(self, put_key, block):
        '''Handle user input for block movement and rotation.

        Args:
            put_key (str):
                User keyboard input.
            block (tuple):
                Current tetromino shape.

        Returns:
            None
        '''
        # print("[req] request_operation_rotate")
        if put_key == KEY_ROTATION_LEFT:
            self.blocks_map.rotation = self.request_operation_rotate_left(block)
        if put_key == KEY_ROTATION_RIGHT:
            self.blocks_map.rotation = self.request_operation_rotate_right(block)

# ▼▼▼ ハードドロップ機能追加 ▼▼▼
    def get_next_position(self, put_key, block):
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
        '''Handle user input for block movement.

        Args:
            put_key (str):
                User keyboard input.

        Returns:
            None

        '''
        # print("[req] get_next_position")
        self.pos.next.x = self.pos.current.x
        self.pos.next.y = self.pos.current.y

        if put_key == KEY_RIGHT:
            self.pos.next.x += 1
        elif put_key == KEY_LEFT:
            self.pos.next.x -= 1
        elif put_key == KEY_DROP:
            self.pos.next.y += 1
# ▼▼▼ ハードドロップ機能追加 ▼▼▼
        elif put_key == KEY_HARD_DROP:
            self.collision.execute_hard_drop(block)
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
        else:
            # Do Nothing
            pass

    def request_operation_rotate_left(self, block):
        '''Rotate block to the left.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            tuple:
                Updated block, x-coordinate, and y-coordinate.
        '''
        # print("[req] request_operation_rotate_left")
        new_rotation = self.blocks_map.rotation - 1
        if new_rotation < 0:
            new_rotation = 3
        
        block_width = self.blocks.get_block_width(block, new_rotation)
        block_height = self.blocks.get_block_height(block, new_rotation)
        if self.pos.current.x + block_width < 0:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.x + block_width > brddc.PlayBoardSize.WIDTH:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.y + block_height < 0:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.y + block_height > brddc.PlayBoardSize.HEIGHT:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = self.blocks_map.rotation

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
        # print("[req] request_operation_rotate_right")
        new_rotation = self.blocks_map.rotation + 1
        new_rotation = new_rotation % 4

        block_width = self.blocks.get_block_width(block, new_rotation)
        block_height = self.blocks.get_block_height(block, new_rotation)
        if self.pos.current.x + block_width< 0:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.x + block_width >= brddc.PlayBoardSize.WIDTH:
            # print(f"x + block_width:{x + block_width}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.y + block_height< 0:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = self.blocks_map.rotation
        if self.pos.current.y + block_height >= brddc.PlayBoardSize.HEIGHT:
            # print(f"x + block_width:{x + block_height}")
            new_rotation = self.blocks_map.rotation

        return new_rotation

    def get_putkey(self):
        return self.put_key
    
    def clear_putkey(self):
        self.put_key = ''

    def input_putkey(self):
        if OS_ENVIROMENT == LINUX:
            self.put_key = self.getch_for_Linux()

        elif OS_ENVIROMENT == WINDOWS:
            if msvcrt.kbhit():
                self.put_key = msvcrt.getch()
        else:
            self.put_key = input()
        # print(f"self.put_key:{self.put_key}")
