#include <stdio.h>
#include <string.h>
#include "board.h"

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/

/*----------------------------*/
/* variable */
/*----------------------------*/
static int board_result[BOARD_HEIGHT][BOARD_WIDTH]; /* 永続状態 */
static int board[BOARD_HEIGHT][BOARD_WIDTH];        /* 描画用 */

/*----------------------------*/
/* function section */
/*----------------------------*/
void initialize_board(int board_value[BOARD_HEIGHT][BOARD_WIDTH]);
void sanitize_board(int board_param[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH]);

/*----------------------------*/
/* public function */
/*----------------------------*/
void update_view(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* printf("[view] update_view\n"); */

    /* view */
    load_board_result();                   /* おばけ(残像)を消す */
    for (int r = 0; r < BLOCK_SIZE_HEIGHT; r++)
    {
        for (int c = 0; c < BLOCK_SIZE_WIDTH; c++)
        {
            if (block[position.rotation][r][c] == BOARD_CELL_OCCUPIED)
            {
                if (position.y + r < 0 || position.y + r >= BOARD_SIZE_HEIGHT ||
                    position.x + c < 0 || position.x + c >= BOARD_SIZE_WIDTH)
                {
                    printf("Warning: Block position is out of board range. (x=%d, y=%d)\n", position.x + c, position.y + r);
                    continue;   /* board の範囲外 */
                }
                board[position.y + r][position.x + c] = BOARD_CELL_OCCUPIED;
            }
        }
    }
    draw_board(board);
}

void update_view_gui(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* printf("[view] update_view\n"); */

    /* view */
    // load_board_result();                   /* おばけ(残像)を消す */
    for (int r = 0; r < BLOCK_SIZE_HEIGHT; r++)
    {
        for (int c = 0; c < BLOCK_SIZE_WIDTH; c++)
        {
            if (block[position.rotation][r][c] == BOARD_CELL_OCCUPIED)
            {
                if (position.y + r < 0 || position.y + r >= BOARD_SIZE_HEIGHT ||
                    position.x + c < 0 || position.x + c >= BOARD_SIZE_WIDTH)
                {
                    printf("Warning: Block position is out of board range. (x=%d, y=%d)\n", position.x + c, position.y + r);
                    continue;   /* board の範囲外 */
                }
                board[position.y + r][position.x + c] = BOARD_CELL_OCCUPIED;
            }
        }
    }
    // draw_board(board);
}

/* board header
 * group board functions
 */
void init_board(void)
{
    /* printf("[init] init_board\n"); */
    create_board();
}

void create_board(void)
{
    /* printf("[init] create_board\n"); */
    initialize_board(board_result);
    initialize_board(board);
}

void load_board_result(void)
{
    /* printf("[init] load_board_result\n"); */
    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++)
    {
        memcpy(board[r], board_result[r], sizeof(int) * BOARD_SIZE_WIDTH);
    }
}

void draw_board(int board_param[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH])
{
    /* printf("[proc] draw_board\n"); */
    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++)
    {
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++)
        {
            if (board_param[r][c] == BOARD_CELL_EMPTY)
            {
                printf("\xE2\x96\xA1"); /* □ */
            } else
            {
                printf("\xE2\x96\xA0"); /* ■ */
            }
        }
        printf("\n");
    }
}

void clear_bingo_lines(void)
{
    int new_board[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH];
    int new_board_count = 0;

    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++)
    {
        int ones = 0;
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++)
        {
            if (board_result[r][c] == BOARD_CELL_OCCUPIED)
            {
                ones++;
            }
        }
        if (ones < BOARD_SIZE_WIDTH)
        {
            memcpy(new_board[new_board_count], board_result[r], sizeof(int) * BOARD_SIZE_WIDTH);
            new_board_count++;
        }
    }

    while (new_board_count < BOARD_SIZE_HEIGHT)
    {
        /* new_board.insert(0, [0]*BOARD_SIZE_WIDTH) 相当 */
        for (int r = new_board_count; r > 0; r--)
        {
            memcpy(new_board[r], new_board[r - 1], sizeof(int) * BOARD_SIZE_WIDTH);
        }
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++)
        {
            new_board[0][c] = BOARD_CELL_EMPTY;
        }
        new_board_count++;
    }

    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++)
    {
        memcpy(board_result[r], new_board[r], sizeof(int) * BOARD_SIZE_WIDTH);
    }
}

bingo_lines_t get_bingo_lines(void)
{
    bingo_lines_t delete_rows;
    delete_rows.count = 0;

    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++)
    {
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++)
        {
            if (board_result[r][c] != BOARD_CELL_OCCUPIED)
            {
                break;
            }
            if (c >= BOARD_SIZE_WIDTH - 1)
            {
                delete_rows.rows[delete_rows.count++] = r;
            }
        }
    }
    return delete_rows;
}

/* 永続状態 */
void set_board_boardresult(const int value[BOARD_HEIGHT][BOARD_WIDTH])
{
    int board_sanitized[BOARD_HEIGHT][BOARD_WIDTH];
    initialize_board(board_sanitized);
    memcpy(board_sanitized, value, sizeof(board_sanitized));
    sanitize_board(board_sanitized);
    memcpy(board_result, board_sanitized, sizeof(board_result));
}

void get_board_boardresult(int value[BOARD_HEIGHT][BOARD_WIDTH])
{
    memcpy(value, board_result, sizeof(board_result));
}

/* 描画用 */
void set_board_boardview(const int value[BOARD_HEIGHT][BOARD_WIDTH])
{
    int board_sanitized[BOARD_HEIGHT][BOARD_WIDTH];
    initialize_board(board_sanitized);
    memcpy(board_sanitized, value, sizeof(board_sanitized));
    sanitize_board(board_sanitized);
    memcpy(board, board_sanitized, sizeof(board));
}

void get_board_boardview(int value[BOARD_HEIGHT][BOARD_WIDTH])
{
    memcpy(value, board, sizeof(board));
}

/*----------------------------*/
/* private function */
/*----------------------------*/
void initialize_board(int board_value[BOARD_HEIGHT][BOARD_WIDTH])
{
    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++)
    {
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++)
        {
            board_value[r][c] = BOARD_CELL_EMPTY;
        }
    }
}

void sanitize_board(int board_param[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH])
{
    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++)
    {
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++)
        {
            if (board_param[r][c] != BOARD_CELL_OCCUPIED)
            {
                /* ブロック有り以外の値はEmptyとする */
                board_param[r][c] = BOARD_CELL_EMPTY;
            }
        }
    }
}