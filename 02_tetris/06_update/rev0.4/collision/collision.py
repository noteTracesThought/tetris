import board.playboard    as brddc

class Collision():
    '''update check header
    update check functions

    Todo:
        * rotate
    '''
    def __init__(self, pos, blocks_map, play_board, Blocks):
        self.pos        = pos
        self.blocks_map = blocks_map
        self.play_board = play_board
        self.blocks     = Blocks

    def is_invalid_position(self, block):
        '''Validate block movement and rotation.

        Correct coordinates to prevent
        movement outside the board.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            tuple:
                Corrected x-coordinate
                and y-coordinate.
        '''
        # print("[check] is_invalid_position")
        is_invalid = False
        is_invalid_move = self.is_out_of_board(block)
        is_invalid_rotate = self.blocks.check_operation_rotate()
        if is_invalid_move or is_invalid_rotate:
            is_invalid = True
        return is_invalid

    def is_out_of_board(self, block):
        '''Check movable range of the block.

        Prevent block movement outside
        the board boundary.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            (bool)
                True  : Under or Over
                False : Within the specified range
        '''
        # print("[check] is_out_of_board")
        is_invalid = False
        block_width = self.blocks.get_block_width(block, self.blocks_map.rotation)
        block_height = self.blocks.get_block_height(block, self.blocks_map.rotation)
        if self.pos.next.x < 0:
            is_invalid = True
        if self.pos.next.y < 0:
            is_invalid = True
        if self.pos.next.x > brddc.PlayBoardSize.WIDTH - block_width:
            is_invalid = True
        if self.pos.next.y > brddc.PlayBoardSize.HEIGHT - block_height:
            is_invalid = True
        return is_invalid

    def check_collision_detection(self, block):
        '''Check if there was a collision with a block.

        Detecting Block Collisions.

        Args:
            block (tuple):
                Current tetromino shape.

        Returns:
            tuple:
                Corrected x-coordinate
                and y-coordinate.
        '''
        # print("[check] check_collision_detection")
        block_width = self.blocks.get_block_width(block, self.blocks_map.rotation)
        block_height = self.blocks.get_block_height(block, self.blocks_map.rotation)
        for r in range(len(block[self.blocks_map.rotation])):
            for c in range(len(block[self.blocks_map.rotation][r])):
                # 衝突検知(床)
                if self.pos.next.y >= brddc.PlayBoardSize.HEIGHT - block_height:
                    # print(f"next_y:{next_y}")
                    return True
                
                # next(blockなし)
                if block[self.blocks_map.rotation][r][c] != 1:
                    continue
                
                # 衝突検知(board block)
                if self.play_board.board_result[self.pos.next.y + r][self.pos.next.x + c] == 1:
                    # print(f"next_y+r:{next_y+r}")
                    # print(f"next_x+c:{next_x+c}")
                    return True
                
                # 衝突検知(next board block)
                if self.play_board.board_result[self.pos.next.y + r + 1][self.pos.next.x + c] == 1:
                    # print(f"next_y+r+1:{next_y+r+1}")
                    # print(f"next_x+c:{next_x+c}")
                    return True
                
        return False

# ▼▼▼ ハードドロップ機能追加 ▼▼▼
    def execute_hard_drop(self, block):
        '''ハードドロップを実行する'''

        while True:
            try:
                # 仮想的に1段下の位置（Position）を計算して next にセットするだけ
                self.pos.next.y += 1
            except ValueError:
                # 盤面の底（PosYの範囲外）に到達したらループ終了
                break
                
            # その1段下（next）で衝突するかチェック
            if self.check_collision_detection(block):
                # ぶつかるなら、今の current（衝突する直前の安全な位置）が最終位置なので終了
                break
                
            # ぶつからなければ、現在位置(current)を1段下に進めて次のループへ
            self.pos.current.y = self.pos.next.y
        self.pos.next.y = self.pos.current.y

# ▲▲▲ ハードドロップ機能追加 ▲▲▲
