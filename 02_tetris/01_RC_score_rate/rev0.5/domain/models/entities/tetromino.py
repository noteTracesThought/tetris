from dataclasses import dataclass

from domain.models.valueobject.position import MovePosition, Position, PosX, PosY
from domain.models.valueobject.block_catalog import Rotation
from block.block import Blocks

@dataclass
class Tetromino:
    shape: tuple
    position: MovePosition
    rotation: Rotation

    def __init__(self, shape: Blocks, pos:MovePosition, rotation: int = 0):
        self.shape:Blocks   = shape
        self.shape.create_blocks()
        self.position       = pos
        self.next_tetromino()

    def next_tetromino(self, x: int = 3, y: int = 0, rotation: int = 0):
        self.position.current   = Position(PosX(x), PosY(y))
        self.position.next      = Position(PosX(x), PosY(y))
        self.rotation           = Rotation(rotation)
        self.current_block      = self.shape.get_block()
        # return self.current_block

    def get_tetromino(self):
        return self.current_block

    def width(self):
        return self.shape.get_block_width(self.current_block, self.rotation.value)
    
    def height(self):
        return self.shape.get_block_height(self.current_block, self.rotation.value)

    def rotate_right(self):
        self.rotation = Rotation(self.rotation.value + 1)

    def rotate_left(self):
        self.rotation = Rotation(self.rotation.value - 1)

    def move(self, position: MovePosition):
        self.position = position

    def fix_tetromino(self):
        self.shape.fix_block(self.current_block, self.position, self.rotation.value)
    
    def get_position(self):
        return self.position
    
    def get_rotation(self):
        return self.rotation.value
    