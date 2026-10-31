#include <stdio.h>
#include <string.h>
#include "board.h"
#include "../settings.h"

void update_view(const int block[4][4][4], int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[view] update_view\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */

    /* view */
    load_board_result();                   /* おばけ(残像)を消す */
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < 4; c++) {
            if (block[rotation][r][c] == 1) {
                board[y + r][x + c] = 1;
                /* printf("r+y: %d\n", r + y); */
                /* printf("c+x: %d\n", c + x); */
            }
        }
    }
    draw_board(board);
}

/* board header
 * group board functions
 */
void init_board(void)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[init] init_board\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    create_board();
}

void create_board(void)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[init] create_board\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++) {
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++) {
            board_result[r][c] = 0;
            board[r][c] = 0;
        }
    }
}

void load_board_result(void)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[init] load_board_result\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++) {
        memcpy(board[r], board_result[r], sizeof(int) * BOARD_SIZE_WIDTH);
    }
}

void draw_board(int board_param[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH])
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[proc] draw_board\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++) {
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++) {
            if (board_param[r][c] == 0) {
                printf("\xE2\x96\xA1"); /* □ */
            } else {
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

    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++) {
        int ones = 0;
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++) {
            if (board_result[r][c] == 1) {
                ones++;
            }
        }
        if (ones < BOARD_SIZE_WIDTH) {
            memcpy(new_board[new_board_count], board_result[r], sizeof(int) * BOARD_SIZE_WIDTH);
            new_board_count++;
        }
    }

    while (new_board_count < BOARD_SIZE_HEIGHT) {
        /* new_board.insert(0, [0]*BOARD_SIZE_WIDTH) 相当 */
        for (int r = new_board_count; r > 0; r--) {
            memcpy(new_board[r], new_board[r - 1], sizeof(int) * BOARD_SIZE_WIDTH);
        }
        for (int c = 0; c < BOARD_SIZE_WIDTH; c++) {
            new_board[0][c] = 0;
        }
        new_board_count++;
    }

    for (int r = 0; r < BOARD_SIZE_HEIGHT; r++) {
        memcpy(board_result[r], new_board[r], sizeof(int) * BOARD_SIZE_WIDTH);
    }
}

BingoLines get_bingo_lines(void)
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
