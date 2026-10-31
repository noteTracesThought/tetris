import time
import settings
from settings import (
    OS_ENVIROMENT,
    LINUX,
    WINDOWS,
    KEY_GAME_FINISH,
    KEY_DROP,
    BOARD_SIZE_WIDTH,
    SCORE_MULTIPLIER
)

from block.block import (
    create_blocks,
    get_block,
    fix_block
)

from board.board import (
    update_view,
    init_board,
    clear_bingo_lines
)

from collision.collision import (
    check_fall_collision,
    adjust_pos
)

from input.input import (
    request_operation_rotate,
    get_next_position,
    get_putkey,
    init_input,
    restore_input,
    input_putkey
)

from cycle.cycle import (
    cycle_init,
    cycle_mainloop
)

from cycle.cycle_process import pop_fall_event

'''tetris main task header
tetris main task functions

Todo:
    * 側面衝突検知時は壁扱いとなるように修正すること
    * ブロックが側面の壁に到達しない
    * 周期タスク処理
'''

is_update = False
CPU_SLEEP     = 0.01         # 10ms

def power_on_game():
    '''Start the Tetris game loop.

    Initialize the game and handle
    user input until quit command.

    Returns:
        None
    '''
    # print("[task] power on")
    init_game()
    init_input()
    cycle_init()

    put_key = ""
    block = get_block()
    x = 3
    y = 0
    score = 0
    rotation = 0
    set_update_view(False)
    while(put_key != KEY_GAME_FINISH):
        input_putkey()
        cycle_mainloop()
        time.sleep(CPU_SLEEP)

        put_key = None
        _put_key = get_putkey()
        if _put_key:
            put_key = _put_key

        rotation = request_operation_rotate(put_key, block, x, y, rotation)
        next_x, next_y = get_next_position(put_key, block, x, y, rotation)

        # 既存ブロック衝突、ボード側面衝突検知
        # if check_move_collision(block, next_x, next_y, rotation):
        #     next_x = x
        #     next_y = y
        next_x, next_y, rotation = adjust_pos(block, next_x, next_y, rotation)

        # 落下衝突検知
        if check_fall_collision(block, next_x, next_y, rotation):
            fix_block(block, next_x, next_y, rotation)  # update board result
            # print(f"x={x}")
            # print(f"y={y}")
            # print(f"next_x={next_x}")
            # print(f"next_y={next_y}")

            # game over
            if is_game_over(put_key) == True:
                print("game over!")
                break

            # bingo
            bingo_lines = get_bingo_lines()
            score += len(bingo_lines) * SCORE_MULTIPLIER[len(bingo_lines)]
            clear_bingo_lines()

            block = get_block()
            # print(block)
            x = 3
            y = 0
            rotation = 0
        else:
            x = next_x
            y = next_y

        # print(rotation)
        # print(block[rotation])
        # print(type(block[rotation]))

        if pop_fall_event():
            set_update_view(True)
            y += 1
        is_update_view(block, x, y, rotation)

    print(f"score : {int(score * 100)}")
    restore_input()

'''initialize header
initialize functions
'''
def init_game():
    '''Initialize game settings.

    Initialize board and block data.

    Returns:
        None
    '''
    # print("[init] initialize")
    init_board()
    create_blocks()

def get_bingo_lines():
    delete_rows = []
    for r in range(len(settings.board_result)):
        for c in range(len(settings.board_result[r])):
            if settings.board_result[r][c] != 1:
                break
            if c >= BOARD_SIZE_WIDTH-1:
                delete_rows.append(r)
                print("bingo!!")
    return delete_rows

def is_game_over(put_key):
    if put_key == KEY_DROP:
        next_y = 1
    else:
        next_y = 0
    for c in range(len(settings.board_result[next_y])):
        if settings.board_result[next_y][c] == 1:
            return True
    return False

def set_update_view(value):
    global is_update
    is_update = value

def is_update_view(block, x, y, rotation):
    global is_update
    if is_update:
        update_view(block, x, y, rotation)
        set_update_view(False)
