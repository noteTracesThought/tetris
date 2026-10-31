import random
import settings

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

class Blocks():
    def create_blocks():
        '''Create tetromino block definitions.

        Initialize block map and key list.

        Returns:
            None
        '''
        print("[init] create_blocks")
        # global block_map_key
        # global block_map
        settings.block_map_key = list()
        settings.block_map = {
                        "I": I,
                        "J": J,
                        "L": L,
                        "S": S,
                        "Z": Z,
                        "O": O,
                        "T": T,
                    }
        for key in settings.block_map.keys():
            settings.block_map_key.append(key)

    def get_block():
        '''Get a random tetromino block.

        Returns:
            tuple:
                Randomly selected block.
        '''
        return (settings.block_map[random.choice(settings.block_map_key)])

    def get_block_width(block, rotation):
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

    def get_block_height(block, rotation):
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

    def check_operation_rotate():
        '''Check block rotation validity.

        Validate whether rotation is
        allowed in the current position.

        Returns:
            None
        '''
        print("[check] check_operation_rotate")
        return False

    def fix_block(block, next_x, next_y, rotation):
        '''Fix the block on the board.

            Store the current block into
            board_result as a fixed block.

            Args:
                block (tuple):
                    Current tetromino shape.
                next_x (int):
                    X-coordinate.
                next_y (int):
                    Y-coordinate.

            Returns:
                None
        '''
        # global board_result
        for r in range(len(block[rotation])):
            for c in range(len(block[rotation][r])):
                if block[rotation][r][c] == 1:
                    settings.board_result[next_y+r][next_x+c] = 1
                    # print("check", y+r, x+c)
