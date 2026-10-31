import random
import block.block_catalog    as blkdc

class Blocks():
    def __init__(self, pos, blocks_map, play_board):
        self.pos        = pos
        self.blocks_map = blocks_map
        self.play_board = play_board

    def create_blocks(self):
        '''Create tetromino block definitions.

        Initialize block map and key list.

        Returns:
            None
        '''
        print("[init] create_blocks")
        # global blocks_map_key
        # global blocks_map
        self.blocks_map.block_map_key = list()
        self.blocks_map.block_map = {
                        "I": blkdc.I,
                        "J": blkdc.J,
                        "L": blkdc.L,
                        "S": blkdc.S,
                        "Z": blkdc.Z,
                        "O": blkdc.O,
                        "T": blkdc.T,
                    }
        for key in self.blocks_map.block_map.keys():
            self.blocks_map.block_map_key.append(key)

    def get_block(self):
        '''Get a random tetromino block.

        Returns:
            tuple:
                Randomly selected block.
        '''
        return (self.blocks_map.block_map[random.choice(self.blocks_map.block_map_key)])

    def get_block_width(self, block, rotation):
        '''Get effective block width.

        Calculate the actual width of a block
        excluding trailing empty cells.

        Args:
            block (tuple):
                Tetromino shape data.

        Returns:
            int:
                Effective width of the block.
        '''
        print("[check] get_block_width")
        width = 0
        for row in block[rotation]:
            for col in range(len(row)):
                if row[col] == 1:
                    width = max(width, col+1)
        return width

    def get_block_height(self, block, rotation):
        '''Get effective block height.

        Calculate the actual height of a block
        excluding trailing empty cells.

        Args:
            block (tuple):
                Tetromino shape data.

        Returns:
            int:
                Effective height of the block.
        '''
        print("[check] get_block_height")
        height = 0
        for row in range(len(block[rotation])):
            if 1 in block[rotation][row]:
                height = row + 1
        return height

    def check_operation_rotate(self):
        '''Check block rotation validity.

        Validate whether rotation is
        allowed in the current position.

        Returns:
            None
        '''
        print("[check] check_operation_rotate")
        # TODO:
        # Rotation validity check may move to Collision.
        # Current implementation keeps compatibility with rev0.3.
        return False

    def fix_block(self, block):
        '''Fix the block on the board.

            Store the current block into
            board_result as a fixed block.

            Args:
                block (tuple):
                    Current tetromino shape.

            Returns:
                None
        '''
        # global board_result
        for r in range(len(block[self.blocks_map.rotation])):
            for c in range(len(block[self.blocks_map.rotation][r])):
                if block[self.blocks_map.rotation][r][c] == 1:
                    self.play_board.board_result[self.pos.next.y + r][self.pos.next.x + c] = 1
                    # print("check", y+r, x+c)
