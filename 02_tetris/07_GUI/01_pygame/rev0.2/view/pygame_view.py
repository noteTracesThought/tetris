import sys
from enum import Enum
import settings
from settings import (
    OS_ENVIROMENT,
    LINUX,
    WINDOWS,
    KEY_GAME_FINISH,
    KEY_DROP,
    BOARD_SIZE_WIDTH,
    BOARD_SIZE_HEIGHT,
    SCORE_MULTIPLIER,
    KEY_LEFT,
    KEY_RIGHT,
    KEY_ROTATION_LEFT,
    KEY_ROTATION_RIGHT,
    KEY_HARD_DROP
)

from block.block import (
    get_block,
    fix_block
)

from board.board import (
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
)

from cycle.cycle import (
    cycle_init,
    cycle_mainloop
)

from cycle.cycle_process import pop_fall_event

import pygame

from game.game import (
    init_game,
    set_update_view,
    is_update_view,
    get_bingo_lines,
    is_game_over
)

'''tetris main task header
tetris main task functions

Todo:
    * status manager to outside function.
      while loop is simple.
    * args is marge to typedef struct.
'''

is_update    = False
FRAME_WIDTH  = 400
FRAME_HEIGHT = 600
CELL_SIZE    = FRAME_HEIGHT / 20
BOARD_X      = FRAME_WIDTH / 20 * 2
BOARD_Y      = 0

class GAME_STATUS_NUMBER(Enum):
    INIT  = 0
    INPUT = 1
    LOGIC = 2
    VIEW  = 3
    QUIT  = 4

INIT_TYPE  = "INIT"
INPUT_TYPE = "INPUT"
LOGIC_TYPE = "LOGIC"
VIEW_TYPE  = "VIEW"
QUIT_TYPE  = "QUIT"

GAME_STATUS  = {
    GAME_STATUS_NUMBER.INIT :INIT_TYPE,
    GAME_STATUS_NUMBER.INPUT:INPUT_TYPE,
    GAME_STATUS_NUMBER.LOGIC:LOGIC_TYPE,
    GAME_STATUS_NUMBER.VIEW :VIEW_TYPE,
    GAME_STATUS_NUMBER.QUIT :QUIT_TYPE
}

# 1. Pygameのキーとゲーム内キーのマッピング辞書を定義
KEY_MAP = {
    pygame.K_s: KEY_LEFT,
    pygame.K_d: KEY_RIGHT,
    pygame.K_r: KEY_ROTATION_RIGHT,
    pygame.K_w: KEY_ROTATION_LEFT,
    pygame.K_SPACE: KEY_DROP,
    pygame.K_h: KEY_HARD_DROP,
    pygame.K_q: KEY_GAME_FINISH,
}

def start():
    '''Start the Tetris game loop.

    Initialize the game and handle
    user input until quit command.

    Returns:
        None
    '''
    # print("[task] power on")
    game_status_now = GAME_STATUS_NUMBER.INIT
    if GAME_STATUS[game_status_now] == INIT_TYPE:
        init_game()
        init_input()
        cycle_init()
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
        pygame.display.set_caption("tetris")

        put_key = ""
        block = get_block()
        x = 3
        y = 0
        score = 0
        rotation = 0
        game_status_now = GAME_STATUS_NUMBER.INPUT

    # メインループ
    running = True
    while running:
        if GAME_STATUS[game_status_now] == INPUT_TYPE:
            # ① pygameから入力を取得
            input_key_pygame()
            put_key = get_putkey()
            if put_key == KEY_GAME_FINISH:
                running = False
                # game_status_now = GAME_STATUS_NUMBER.QUIT
                continue
            game_status_now = GAME_STATUS_NUMBER.LOGIC

                # for event in pygame.event.get():
                #     if event.type == pygame.QUIT:
                #         running = False

        elif GAME_STATUS[game_status_now] == LOGIC_TYPE:
            # ゲームロジック
            # ② 今まで作ったゲームロジックを実行
            cycle_mainloop()

            if pop_fall_event():
                set_update_view(True)
                y += 1
            is_update_view(block, x, y, rotation)

            # if put_key is not None:
            rotation = request_operation_rotate(
                put_key,
                block,
                x,
                y,
                rotation
            )

            next_x, next_y = get_next_position(
                put_key,
                block,
                x,
                y,
                rotation
            )

            next_x, next_y, rotation = adjust_pos(
                block,
                next_x,
                next_y,
                rotation
            )

            # ③ 衝突判定
            if check_fall_collision(
                block,
                next_x,
                next_y,
                rotation
            ):
                fix_block(
                    block,
                    next_x,
                    next_y,
                    rotation
                )
                # game over
                if is_game_over(put_key) == True:
                    print("game over!")
                    game_status_now = GAME_STATUS_NUMBER.QUIT
                    break

                # bingo
                bingo_lines = get_bingo_lines()
                score += len(bingo_lines) * SCORE_MULTIPLIER[len(bingo_lines)]
                clear_bingo_lines()

                block = get_block()
                x = 3
                y = 0
                rotation = 0

            else:
                x = next_x
                y = next_y

            game_status_now = GAME_STATUS_NUMBER.VIEW

        elif GAME_STATUS[game_status_now] == VIEW_TYPE:
            # ④ pygameで描画
            draw_game(
                screen,
                # settings.board_result,
                block,
                x,
                y,
                rotation
                # score
            )
            clock.tick(60)
            game_status_now = GAME_STATUS_NUMBER.INPUT

        elif GAME_STATUS[game_status_now] == QUIT_TYPE:
            # ゲーム終了
            running = False

        else:
            # Do Nothing
            game_status_now = GAME_STATUS_NUMBER.INPUT

    if GAME_STATUS[game_status_now] == QUIT_TYPE:
        # ゲーム終了
        print(score * 100)
        pygame.quit()
        sys.exit()


def draw_board_pygame(screen):
    for r in range(BOARD_SIZE_HEIGHT):
        for c in range(BOARD_SIZE_WIDTH):

            px = BOARD_X + c * CELL_SIZE
            py = BOARD_Y + r * CELL_SIZE

            if settings.board_result[r][c] == 1:
                color = (0, 200, 255)
            else:
                color = (30, 30, 30)

            pygame.draw.rect(
                screen,
                color,
                (px, py, CELL_SIZE, CELL_SIZE)
            )

def draw_game(screen, block, x, y, rotation):
    screen.fill((0, 0, 0))
    draw_board_pygame(screen)
    draw_current_block(
        screen,
        block,
        x,
        y,
        rotation
    )
    pygame.display.flip()

def input_key_pygame():
    for event in pygame.event.get():

        # クローズボタン（×ボタン）が押された場合
        if event.type == pygame.QUIT:
            settings.put_key = KEY_GAME_FINISH
            return  # 終了時は即座に抜ける

        # キーボードが押された場合
        if event.type == pygame.KEYDOWN:
            # 辞書から対応するキーを取得（登録がないキーなら None）
            settings.put_key = KEY_MAP.get(event.key, None)

def draw_current_block(screen, block, x, y, rotation):

    current_block = block[rotation]

    for r in range(len(current_block)):
        for c in range(len(current_block[r])):

            if current_block[r][c] != 1:
                continue

            px = BOARD_X + (x + c) * CELL_SIZE
            py = BOARD_Y + (y + r) * CELL_SIZE

            pygame.draw.rect(
                screen,
                (255, 100, 100),
                (px, py, CELL_SIZE, CELL_SIZE)
            )

    # # CPU高負荷用
    # for i in range(100000):
    #     pygame.draw.rect(screen, (255, 255, 255, 10), (0, 0, 10, 10))
