from settings import (
    KEY_GAME_FINISH,
    KEY_DROP,
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
    clear_bingo_lines,
    get_bingo_lines,
    get_board_result
)

from collision.collision import (
    check_fall_collision,
    check_move_collision,
    adjust_pos
)

from input.input import (
    request_operation_rotate,
    get_next_position,
    get_putkey,
    init_input,
    restore_input,
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
        cycle_mainloop()

        put_key = None
        _put_key = get_putkey()
        if _put_key:
            put_key = _put_key

        fall_event = pop_fall_event()
        next_rotation = request_operation_rotate(put_key, block, x, y, rotation)
        next_x, next_y = get_next_position(put_key, block, x, y, next_rotation)
        if fall_event:
            next_y += 1

        # 既存ブロック衝突、ボード側面衝突検知
        next_x, next_y, next_rotation = adjust_pos(block, next_x, next_y, next_rotation)
        if check_move_collision(block, next_x, next_y, next_rotation):
            next_x, next_y, next_rotation = x, y, rotation

        # 落下衝突検知
        if check_fall_collision(block, next_x, next_y, next_rotation):
            fix_x, fix_y, fix_rotation = (
                (x, y, rotation)
                if check_move_collision(block, next_x, next_y, next_rotation)
                else (next_x, next_y, next_rotation)
            )
            if not fix_block(block, fix_x, fix_y, fix_rotation):
                raise RuntimeError("Unable to fix block at a valid position")
            set_update_view(True)

            # game over
            if is_game_over(put_key) == True:
                print("game over!")
                break

            # bingo
            bingo_lines = get_bingo_lines()
            if bingo_lines:
                print("bingo!!")
            score += len(bingo_lines) * SCORE_MULTIPLIER[len(bingo_lines)]
            clear_bingo_lines()

            block = get_block()
            x = 3
            y = 0
            rotation = 0
        else:
            x = next_x
            y = next_y
            rotation = next_rotation

        if fall_event:
            set_update_view(True)
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

def is_game_over(put_key):
    if put_key == KEY_DROP:
        next_y = 1
    else:
        next_y = 0
    board_result = get_board_result()
    for cell in board_result[next_y]:
        if cell == 1:
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
