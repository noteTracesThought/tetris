#include <stdio.h>
#include "collision.h"
#include "../settings.h"
#include "../board/board.h"

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/
/* 壁蹴りのX座標補正範囲(3ブロック分) */
#define WALL_KICK_INDEX 7
static const int WALL_KICK_X[WALL_KICK_INDEX] =
{
    0, -1, 1, -2, 2, -3, 3
};

/*----------------------------*/
/* variable */
/*----------------------------*/

/*----------------------------*/
/* function section */
/*----------------------------*/
bool can_place(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position);

/*----------------------------*/
/* public function */
/*----------------------------*/
bool is_invalid_position(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* printf("[check] is_invalid_position\n"); */
    bool is_invalid = false;
    bool is_invalid_move = is_out_of_board(block, position);
    bool is_invalid_rotate = check_operation_rotate();
    if (is_invalid_move || is_invalid_rotate)
    {
        is_invalid = true;
    }
    return is_invalid;
}

bool is_out_of_board(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* printf("[check] is_out_of_board\n"); */
    /* 盤面外 */
    if (position.rotation < 0 || position.rotation >= ROUTATION_COUNT)
    {
        return true;
    }

    for (int r = 0; r < BLOCK_SIZE_HEIGHT; r++)
    {
        for (int c = 0; c < BLOCK_SIZE_WIDTH; c++)
        {
            if (block[position.rotation][r][c] != 1)
            {
                continue;
            }

            int board_x = position.x + c;
            int board_y = position.y + r;

            /* 盤面外 */
            if (board_x < 0 || board_x >= BOARD_SIZE_WIDTH ||
                board_y < 0 || board_y >= BOARD_SIZE_HEIGHT)
            {
                return true;
            }
        }
    }
    return false;
}

/* 移動先の衝突確認＋ボード末端確認 */
bool check_fall_collision(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* printf("[check] check_fall_collision\n"); */
    if(check_move_collision(block, position) == true)
    {
        return true;
    }

    position.y++;
    return check_move_collision(block, position);
}

/* 移動先の衝突確認 */
bool check_move_collision(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* printf("[check] check_move_collision\n"); */
    if(can_place(block, position) == false)
    {
        return true;
    }
    return false;
}

bool adjust_pos(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t *position)
{
    for(int index = 0; index < WALL_KICK_INDEX; index++)
    {
        common_pos_t candidate = *position;
        candidate.x += WALL_KICK_X[index];
        if(check_move_collision(block, candidate) == false)
        {
            *position = candidate;
            return true;
        }
    }
    return false;
}

common_pos_t execute_hard_drop(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* ハードドロップを実行する */
    common_pos_t current = position;
    common_pos_t next = position;

    while (true)
    {
        /* 仮想的に1段下の位置（Position）を計算して next にセットするだけ */
        next.y += 1;

        /* その1段下（next）で衝突するかチェック */
        if (check_fall_collision(block, next) == true)
        {
            /* ぶつかるなら、今の current（衝突する直前の安全な位置）が最終位置なので終了 */
            break;
        }

        /* ぶつからなければ、現在位置(current)を1段下に進めて次のループへ */
        current = next;
    }
    return current;
}

/*----------------------------*/
/* private function */
/*----------------------------*/
bool can_place(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* printf("[check] check_move_collision\n"); */
    /* 盤面外 */
    if (is_out_of_board(block, position) == true)
    {
        return false;
    }

    const int (*current_block)[BLOCK_SIZE_WIDTH] = block[position.rotation];
    int board_result[BOARD_HEIGHT][BOARD_WIDTH];
    get_board_boardresult(board_result);

    for (int r = 0; r < BLOCK_SIZE_HEIGHT; r++)
    {
        for (int c = 0; c < BLOCK_SIZE_WIDTH; c++)
        {
            if (current_block[r][c] != 1)
            {
                continue;
            }

            /* 既存ブロックとの衝突 */
            int board_x = position.x + c;
            int board_y = position.y + r;
            if (board_result[board_y][board_x] == 1)
            {
                return false;
            }
        }
    }

    return true;
}