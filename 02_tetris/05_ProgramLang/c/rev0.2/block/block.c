#include <stdlib.h>
#include "block.h"
#include "../settings.h"

/* 各ブロックは [rotation(TOP,RIGHT,BOTTOM,LEFT)][row][col] の順で定義 */
static const int I[4][4][4] = {
    {{1,1,1,1},{0,0,0,0},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,1},{0,0,0,1},{0,0,0,1},{0,0,0,1}},
    {{0,0,0,0},{0,0,0,0},{0,0,0,0},{1,1,1,1}},
    {{1,0,0,0},{1,0,0,0},{1,0,0,0},{1,0,0,0}}
};

static const int J[4][4][4] = {
    {{0,1,1,1},{0,0,0,1},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,0,1},{0,0,0,1},{0,0,1,1}},
    {{0,0,0,0},{0,0,0,0},{1,0,0,0},{1,1,1,0}},
    {{1,1,0,0},{1,0,0,0},{1,0,0,0},{0,0,0,0}}
};

static const int L[4][4][4] = {
    {{1,1,1,0},{1,0,0,0},{0,0,0,0},{0,0,0,0}},
    {{0,0,1,1},{0,0,0,1},{0,0,0,1},{0,0,0,0}},
    {{0,0,0,0},{0,0,0,0},{0,0,0,1},{0,1,1,1}},
    {{0,0,0,0},{1,0,0,0},{1,0,0,0},{1,1,0,0}}
};

static const int S[4][4][4] = {
    {{0,0,1,1},{0,1,1,0},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,1,0},{0,0,1,1},{0,0,0,1}},
    {{0,0,0,0},{0,0,0,0},{0,1,1,0},{1,1,0,0}},
    {{1,0,0,0},{1,1,0,0},{0,1,0,0},{0,0,0,0}}
};

static const int Z[4][4][4] = {
    {{0,1,1,0},{0,0,1,1},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,0,1},{0,0,1,1},{0,0,1,0}},
    {{0,0,0,0},{0,0,0,0},{1,1,0,0},{0,1,1,0}},
    {{0,1,0,0},{1,1,0,0},{1,0,0,0},{0,0,0,0}}
};

static const int O[4][4][4] = {
    {{0,0,1,1},{0,0,1,1},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,0,0},{0,0,1,1},{0,0,1,1}},
    {{0,0,0,0},{0,0,0,0},{1,1,0,0},{1,1,0,0}},
    {{1,1,0,0},{1,1,0,0},{0,0,0,0},{0,0,0,0}}
};

static const int T[4][4][4] = {
    {{0,0,1,0},{0,1,1,1},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,1,0},{0,0,1,1},{0,0,1,0}},
    {{0,0,0,0},{0,0,0,0},{1,1,1,0},{0,1,0,0}},
    {{0,1,0,0},{1,1,0,0},{0,1,0,0},{0,0,0,0}}
};

/* global (settings.py の block_map_key / block_map に相当) */
char block_map_key[BLOCK_MAP_SIZE];
int  block_map_key_count = 0;
block_map_entry_t block_map[BLOCK_MAP_SIZE];

void create_blocks(void)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[init] create_blocks\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    block_map_key_count = 0;

    block_map[0].key = 'I'; block_map[0].shape = I;
    block_map[1].key = 'J'; block_map[1].shape = J;
    block_map[2].key = 'L'; block_map[2].shape = L;
    block_map[3].key = 'S'; block_map[3].shape = S;
    block_map[4].key = 'Z'; block_map[4].shape = Z;
    block_map[5].key = 'O'; block_map[5].shape = O;
    block_map[6].key = 'T'; block_map[6].shape = T;

    for (int i = 0; i < BLOCK_MAP_SIZE; i++) {
        block_map_key[block_map_key_count++] = block_map[i].key;
    }

    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    srand(1234567);
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
}

const int (*get_block(void))[4][4]
{
    int index = rand() % block_map_key_count;
    char selected_key = block_map_key[index];

    for (int i = 0; i < BLOCK_MAP_SIZE; i++) {
        if (block_map[i].key == selected_key) {
            return block_map[i].shape;
        }
    }
    return NULL;
}

int get_block_width(const int block[4][4][4], int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[check] get_block_width\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int width = 0;
    for (int row = 0; row < 4; row++) {
        for (int col = 0; col < 4; col++) {
            if (block[rotation][row][col] == 1) {
                if (col + 1 > width) {
                    width = col + 1;
                }
            }
        }
    }
    return width;
}

int get_block_height(const int block[4][4][4], int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[check] get_block_height\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int height = 0;
    for (int row = 0; row < 4; row++) {
        bool has_block = false;
        for (int col = 0; col < 4; col++) {
            if (block[rotation][row][col] == 1) {
                has_block = true;
                break;
            }
        }
        if (has_block) {
            height = row + 1;
        }
    }
    return height;
}

bool check_operation_rotate(void)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[check] check_operation_rotate\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    return false;
}

void fix_block(const int block[4][4][4], int x, int y, int rotation)
{
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < 4; c++) {
            if (block[rotation][r][c] == 1) {
                board_result[y + r][x + c] = 1;
                /* printf("check %d %d\n", y + r, x + c); */
            }
        }
    }
}
