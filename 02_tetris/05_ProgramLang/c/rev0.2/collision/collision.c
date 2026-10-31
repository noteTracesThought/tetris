#include "collision.h"
#include "../settings.h"
#include "../block/block.h"

bool is_invalid_position(const int block[4][4][4], int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[check] is_invalid_position\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    bool is_invalid = false;
    bool is_invalid_move = is_out_of_board(block, x, y, rotation);
    bool is_invalid_rotate = check_operation_rotate();
    if (is_invalid_move || is_invalid_rotate) {
        is_invalid = true;
    }
    return is_invalid;
}

bool is_out_of_board(const int block[4][4][4], int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[check] is_out_of_board\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    bool is_invalid = false;
    int block_width = get_block_width(block, rotation);
    int block_height = get_block_height(block, rotation);
    if (x < 0) {
        is_invalid = true;
    }
    if (y < 0) {
        is_invalid = true;
    }
    if (x > BOARD_SIZE_WIDTH - block_width) {
        is_invalid = true;
    }
    if (y > BOARD_SIZE_HEIGHT - block_height) {
        is_invalid = true;
    }
    return is_invalid;
}

bool check_collision_detection(const int block[4][4][4], int next_x, int next_y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[check] check_collision_detection\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int block_height = get_block_height(block, rotation);

    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < 4; c++) {
            /* 衝突検知(床) */
            if (next_y >= BOARD_SIZE_HEIGHT - block_height) {
                /* printf("next_y:%d\n", next_y); */
                return true;
            }

            /* next(blockなし) */
            if (block[rotation][r][c] != 1) {
                continue;
            }

            /* 衝突検知(board block) */
            if (board_result[next_y + r][next_x + c] == 1) {
                /* printf("next_y+r:%d\n", next_y + r); */
                /* printf("next_x+c:%d\n", next_x + c); */
                return true;
            }

            /* 衝突検知(next board block) */
            if (board_result[next_y + r + 1][next_x + c] == 1) {
                /* printf("next_y+r+1:%d\n", next_y + r + 1); */
                /* printf("next_x+c:%d\n", next_x + c); */
                return true;
            }
        }
    }

    return false;
}

/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
int execute_hard_drop(const int block[4][4][4], int x, int y, int rotation)
{
    /* ハードドロップを実行する */
    int current_y = y;
    int next_y = y;

    for (;;) {
        /* 仮想的に1段下の位置（Position）を計算して next にセットするだけ
         * (Python版のtry/exceptは実質到達しないため、単純なループとして実装)
         */
        next_y += 1;

        /* その1段下（next）で衝突するかチェック */
        if (check_collision_detection(block, x, next_y, rotation)) {
            /* ぶつかるなら、今の current（衝突する直前の安全な位置）が最終位置なので終了 */
            break;
        }

        /* ぶつからなければ、現在位置(current)を1段下に進めて次のループへ */
        current_y = next_y;
    }
    next_y = current_y;

    return next_y;
}
/* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
