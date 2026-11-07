#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "block.h"
#include "../settings.h"
#include "../board/board.h"

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/
/* 各ブロックは [rotation(TOP,RIGHT,BOTTOM,LEFT)][row][col] の順で定義 */
static const int I[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH] = {
    {{1,1,1,1},{0,0,0,0},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,1},{0,0,0,1},{0,0,0,1},{0,0,0,1}},
    {{0,0,0,0},{0,0,0,0},{0,0,0,0},{1,1,1,1}},
    {{1,0,0,0},{1,0,0,0},{1,0,0,0},{1,0,0,0}}
};

static const int J[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH] = {
    {{0,1,1,1},{0,0,0,1},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,0,1},{0,0,0,1},{0,0,1,1}},
    {{0,0,0,0},{0,0,0,0},{1,0,0,0},{1,1,1,0}},
    {{1,1,0,0},{1,0,0,0},{1,0,0,0},{0,0,0,0}}
};

static const int L[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH] = {
    {{1,1,1,0},{1,0,0,0},{0,0,0,0},{0,0,0,0}},
    {{0,0,1,1},{0,0,0,1},{0,0,0,1},{0,0,0,0}},
    {{0,0,0,0},{0,0,0,0},{0,0,0,1},{0,1,1,1}},
    {{0,0,0,0},{1,0,0,0},{1,0,0,0},{1,1,0,0}}
};

static const int S[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH] = {
    {{0,0,1,1},{0,1,1,0},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,1,0},{0,0,1,1},{0,0,0,1}},
    {{0,0,0,0},{0,0,0,0},{0,1,1,0},{1,1,0,0}},
    {{1,0,0,0},{1,1,0,0},{0,1,0,0},{0,0,0,0}}
};

static const int Z[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH] = {
    {{0,1,1,0},{0,0,1,1},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,0,1},{0,0,1,1},{0,0,1,0}},
    {{0,0,0,0},{0,0,0,0},{1,1,0,0},{0,1,1,0}},
    {{0,1,0,0},{1,1,0,0},{1,0,0,0},{0,0,0,0}}
};

static const int O[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH] = {
    {{0,0,1,1},{0,0,1,1},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,0,0},{0,0,1,1},{0,0,1,1}},
    {{0,0,0,0},{0,0,0,0},{1,1,0,0},{1,1,0,0}},
    {{1,1,0,0},{1,1,0,0},{0,0,0,0},{0,0,0,0}}
};

static const int T[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH] = {
    {{0,0,1,0},{0,1,1,1},{0,0,0,0},{0,0,0,0}},
    {{0,0,0,0},{0,0,1,0},{0,0,1,1},{0,0,1,0}},
    {{0,0,0,0},{0,0,0,0},{1,1,1,0},{0,1,0,0}},
    {{0,1,0,0},{1,1,0,0},{0,1,0,0},{0,0,0,0}}
};

/*----------------------------*/
/* variable */
/*----------------------------*/
/* global (settings.py の block_map_key / block_map に相当) */
static block_map_entry_t block_map[BLOCK_MAP_SIZE];
static int block_bag[BLOCK_MAP_SIZE];
static int block_bag_remaining = 0;
static bool random_seeded = false;

/*----------------------------*/
/* function section */
/*----------------------------*/
void refill_block_bag(void);

/*----------------------------*/
/* public function */
/*----------------------------*/
void create_blocks(void)
{
    /* printf("[init] create_blocks\n"); */
    block_bag_remaining = 0;

    /* const int (*shape)[BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH]; */
    // block_map[0].key = 'I'; block_map[0].shape = I;
    // block_map[1].key = 'J'; block_map[1].shape = J;
    // block_map[2].key = 'L'; block_map[2].shape = L;
    // block_map[3].key = 'S'; block_map[3].shape = S;
    // block_map[4].key = 'Z'; block_map[4].shape = Z;
    // block_map[5].key = 'O'; block_map[5].shape = O;
    // block_map[6].key = 'T'; block_map[6].shape = T;

    /* 記述統一のための犠牲。int shape[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH]; */
    block_map[0].key = 'I';
    memcpy(block_map[0].shape, I, sizeof I);

    block_map[1].key = 'J';
    memcpy(block_map[1].shape, J, sizeof J);

    block_map[2].key = 'L';
    memcpy(block_map[2].shape, L, sizeof L);

    block_map[3].key = 'S';
    memcpy(block_map[3].shape, S, sizeof S);

    block_map[4].key = 'Z';
    memcpy(block_map[4].shape, Z, sizeof Z);

    block_map[5].key = 'O';
    memcpy(block_map[5].shape, O, sizeof O);

    block_map[6].key = 'T';
    memcpy(block_map[6].shape, T, sizeof T);

    if (!random_seeded)
    {
        srand((unsigned int)time(NULL));
        random_seeded = true;
    }
}

void get_block(int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    if (block_bag_remaining == 0)
    {
        refill_block_bag();
    }

    int index = block_bag[--block_bag_remaining];
    for (int p = 0; p < ROUTATION_COUNT; p++)
    {
        for (int r = 0; r < BLOCK_SIZE_HEIGHT; r++)
        {
            for (int c = 0; c < BLOCK_SIZE_WIDTH; c++)
            {
                block[p][r][c] = block_map[index].shape[p][r][c];
            }
        }
    }
}

int get_block_width(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* printf("[check] get_block_width\n"); */
    int width = 0;
    for (int row = 0; row < BLOCK_SIZE_HEIGHT; row++)
    {
        for (int col = 0; col < BLOCK_SIZE_WIDTH; col++)
        {
            if (block[position.rotation][row][col] == 1)
            {
                if (col + 1 > width)
                {
                    width = col + 1;
                }
            }
        }
    }
    return width;
}

int get_block_height(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    /* printf("[check] get_block_height\n"); */
    int height = 0;
    for (int row = 0; row < BLOCK_SIZE_HEIGHT; row++)
    {
        bool has_block = false;
        for (int col = 0; col < BLOCK_SIZE_WIDTH; col++)
        {
            if (block[position.rotation][row][col] == 1)
            {
                has_block = true;
                break;
            }
        }
        if (has_block)
        {
            height = row + 1;
        }
    }
    return height;
}

bool check_operation_rotate(void)
{
    /* printf("[check] check_operation_rotate\n"); */
    return false;
}

void fix_block(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    int board_result[BOARD_HEIGHT][BOARD_WIDTH];
    get_board_boardresult(board_result);

    for (int r = 0; r < BLOCK_SIZE_HEIGHT; r++)
    {
        for (int c = 0; c < BLOCK_SIZE_WIDTH; c++)
        {
            if (block[position.rotation][r][c] == 1)
            {
                board_result[position.y + r][position.x + c] = 1;
                /* printf("check %d %d\n", position.y + r, position.x + c); */
            }
        }
    }
    set_board_boardresult(board_result);
}

/*----------------------------*/
/* private function */
/*----------------------------*/
void refill_block_bag(void)
{
    for (int i = 0; i < BLOCK_MAP_SIZE; i++)
    {
        block_bag[i] = i;
    }

    for (int i = BLOCK_MAP_SIZE - 1; i > 0; i--)
    {
        int j = rand() % (i + 1);
        int temp = block_bag[i];
        block_bag[i] = block_bag[j];
        block_bag[j] = temp;
    }

    block_bag_remaining = BLOCK_MAP_SIZE;
}
