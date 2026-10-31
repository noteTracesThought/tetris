import settings
from settings import BOARD_SIZE_WIDTH, \
                     BOARD_SIZE_HEIGHT

from block.block import Blocks

class Collision():
    '''update check header
    update check functions

    Todo:
        * rotate
    '''
    def is_invalid_position(block, next_x, next_y, rotation):
        '''Validate block movement and rotation.

        Correct coordinates to prevent
        movement outside the board.

        Args:
            block (tuple):
                Current tetromino shape.
            next_x (int):
                Updated x-coordinate.
            next_y (int):
                Updated y-coordinate.

        Returns:
            tuple:
                Corrected x-coordinate
                and y-coordinate.
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[check] is_invalid_position")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        is_invalid = False
        is_invalid_move = Collision.is_out_of_board(block, next_x, next_y, rotation)
        is_invalid_rotate = Blocks.check_operation_rotate()
        if is_invalid_move or is_invalid_rotate:
            is_invalid = True
        return is_invalid

    def is_out_of_board(block, next_x, next_y, rotation):
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
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[check] is_out_of_board")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        is_invalid = False
        block_width = Blocks.get_block_width(block, rotation)
        block_height = Blocks.get_block_height(block, rotation)
        if next_x < 0:
            is_invalid = True
        if next_y < 0:
            is_invalid = True
        if next_x > BOARD_SIZE_WIDTH-block_width:
            is_invalid = True
        if next_y > BOARD_SIZE_HEIGHT-block_height:
            is_invalid = True
        return is_invalid

    def check_collision_detection(block, next_x, next_y, rotation):
        '''Check if there was a collision with a block.

        Detecting Block Collisions.

        Args:
            block (tuple):
                Current tetromino shape.
            next_x (int):
                X-coordinate.
            next_y (int):
                Y-coordinate.

        Returns:
            tuple:
                Corrected x-coordinate
                and y-coordinate.
        '''
        # ▼▼▼ 処理速度計測（10万回） ▼▼▼
        # print("[check] check_collision_detection")
        # ▲▲▲ 処理速度計測（10万回） ▲▲▲
        block_width = Blocks.get_block_width(block, rotation)
        block_height = Blocks.get_block_height(block, rotation)
        for r in range(len(block[rotation])):
            for c in range(len(block[rotation][r])):
                # 衝突検知(床)
                if next_y >= BOARD_SIZE_HEIGHT - block_height:
                    # print(f"next_y:{next_y}")
                    return True
                
                # next(blockなし)
                if block[rotation][r][c] != 1:
                    continue
                
                # 衝突検知(board block)
                if settings.board_result[next_y+r][next_x+c] == 1:
                    # print(f"next_y+r:{next_y+r}")
                    # print(f"next_x+c:{next_x+c}")
                    return True
                
                # 衝突検知(next board block)
                if settings.board_result[next_y+r+1][next_x+c] == 1:
                    # print(f"next_y+r+1:{next_y+r+1}")
                    # print(f"next_x+c:{next_x+c}")
                    return True
                
        return False

# ▼▼▼ ハードドロップ機能追加 ▼▼▼
    def execute_hard_drop(block, x, y, rotation):
        '''ハードドロップを実行する'''
        current_y = y
        next_y = y

        while True:
            try:
                # 仮想的に1段下の位置（Position）を計算して next にセットするだけ
                next_y += 1
            except ValueError:
                # 盤面の底（PosYの範囲外）に到達したらループ終了
                break
                
            # その1段下（next）で衝突するかチェック
            if Collision.check_collision_detection(block, x, next_y, rotation):
                # ぶつかるなら、今の current（衝突する直前の安全な位置）が最終位置なので終了
                break
                
            # ぶつからなければ、現在位置(current)を1段下に進めて次のループへ
            current_y = next_y
        next_y = current_y

        return next_y

# ▲▲▲ ハードドロップ機能追加 ▲▲▲
