#include <stdio.h>
#include <string.h>
#include "../settings.h"
#include "../block/block.h"
#include "../board/board.h"
#include "../collision/collision.h"
#include "../input/input.h"
#include "game.h"

#if defined(__linux__)
/* Do Nothing (input.c 側でインクルード済み) */
#elif defined(_WIN32)
#include <conio.h>
#else
/* Do Nothing */
#endif

/* game.py では board.board から get_bingo_lines を import した後、
 * モジュール末尾で同名の get_bingo_lines() を再定義しているため、
 * power_on_game() 内ではこのローカル版(board側とロジックは同一)が使用される。
 * C言語では同一ファイル内に同名の関数を(staticでも)二重定義できないため、
 * ここだけ game_get_bingo_lines という名前にして再現する。 */
static BingoLines game_get_bingo_lines(void);

static long collision_count = 0;
static long bingo_count = 0;
static long block_count = 0;
static long fix_count = 0;
static long rotate_count = 0;

void power_on_game(void)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[task] power on\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    init_game();

    char put_key = '\0';
    const int (*block)[4][4] = get_block();
    block_count++;
    int x = 3;
    int y = 0;
    double score = 0;
    int rotation = 0;
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    int proc_cnt = 0;
    char commands[6] = {
        KEY_DROP,
        KEY_LEFT,
        KEY_RIGHT,
        KEY_ROTATION_LEFT,
        KEY_ROTATION_RIGHT,
        KEY_HARD_DROP,
    };
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    while (put_key != KEY_GAME_FINISH) {

        /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
        if (0) {
            if (strcmp(OS_ENVIROMENT, LINUX) == 0) {
                put_key = getch_for_Linux();
            } else if (strcmp(OS_ENVIROMENT, WINDOWS) == 0) {
#if defined(_WIN32)
                if (_kbhit()) {
                    put_key = (char)_getch();
                }
#endif
            } else {
                put_key = (char)getchar();
            }
        } else {
            if (proc_cnt < 1000000) {
                put_key = commands[proc_cnt % 6];
                proc_cnt += 1;
            } else {
                break;              /* 10万回計測完了 */
            }
        }
        /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */

        rotation = request_operation_rotate(put_key, block, x, y, rotation);
        rotate_count++;
        /* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
        int next_x, next_y;
        get_next_position(put_key, block, x, y, rotation, &next_x, &next_y);
        /* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
        if (is_invalid_position(block, next_x, next_y, rotation)) {
            next_x = x;
            next_y = y;
        }

        /* 衝突検知 */
        if (check_collision_detection(block, next_x, next_y, rotation)) {
            collision_count++;
            fix_block(block, next_x, next_y, rotation);  /* update board result */
            fix_count++;
            /* printf("x=%d\n", x); */
            /* printf("y=%d\n", y); */
            /* printf("next_x=%d\n", next_x); */
            /* printf("next_y=%d\n", next_y); */

            /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
            /* game over */
            /* if (is_game_over(put_key) == true) { */
            /*     printf("game over!\n"); */
            /*     break; */
            /* } */
            /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */

            /* bingo */
            BingoLines bingo_lines = game_get_bingo_lines();
            /* ▼▼▼ 処理速度が影響していた処理を追加 ▼▼▼ */
            if (bingo_lines.count > 0) {
                bingo_count++;
            /* ▲▲▲ 処理速度が影響していた処理を追加 ▲▲▲ */
                /* ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼ */
                /* score += len(bingo_lines); */
                score += bingo_lines.count * SCORE_MULTIPLIER[bingo_lines.count];
                /* ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲ */
                clear_bingo_lines();
            }

            block = get_block();
            block_count++;
            /* printf("%p\n", (void *)block); */
            x = 3;
            y = 0;
            rotation = 0;
        } else {
            x = next_x;
            y = next_y;
        }

        /* printf("%d\n", rotation); */
        /* printf("%p\n", (void *)block[rotation]); */
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
        /* update_view(block, x, y, rotation); */
    }
    /* printf("score : %f\n", score * 100); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    // measurement_print();
}

/* initialize header
 * initialize functions
 */
void init_game(void)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[init] initialize\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    init_board();
    create_blocks();
}

static BingoLines game_get_bingo_lines(void)
{
    BingoLines delete_rows;
    delete_rows.count = 0;

    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++) {
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++) {
            if (board_result[r][c] != 1) {
                break;
            }
            if (c >= BOARD_SIZE_WIDTH - 1) {
                delete_rows.rows[delete_rows.count++] = r;
                printf("bingo!!\n");
            }
        }
    }
    return delete_rows;
}

bool is_game_over(char put_key)
{
    int next_y;
    if (put_key == KEY_DROP) {
        next_y = 1;
    } else {
        next_y = 0;
    }
    for (int c = 0; c < BOARD_SIZE_WIDTH; c++) {
        if (board_result[next_y][c] == 1) {
            return true;
        }
    }
    return false;
}

void measurement_print()
{
    printf("collision = %ld\n", collision_count);
    printf("bingo     = %ld\n", bingo_count);
    printf("block     = %ld\n", block_count);
    printf("fix       = %ld\n", fix_count);
    printf("rotate    = %ld\n", rotate_count);
}