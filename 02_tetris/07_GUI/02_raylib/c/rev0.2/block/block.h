#ifndef BLOCK_H
#define BLOCK_H

#include <stdbool.h>
#include "../common/common.h"

/*----------------------------*/
/* const */
/*----------------------------*/
#define BLOCK_MAP_SIZE      7
#define ROUTATION_COUNT     4
#define BLOCK_SIZE_HEIGHT   4
#define BLOCK_SIZE_WIDTH    4

/*----------------------------*/
/* type */
/*----------------------------*/
/* テトロミノ1個分の形状データ [rotation][row][col] */
typedef int BlockShape[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH];

/* block_map の1エントリ (Pythonの dict の key-value に相当) */
typedef struct
{
    char key;
    int shape[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH];   /* BlockShape へのポインタ */
} block_map_entry_t;

/*----------------------------*/
/* variable */
/*----------------------------*/

/*----------------------------*/
/* public function */
/*----------------------------*/
void create_blocks(void);
void get_block(int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position);
int get_block_width(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position);
int get_block_height(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position);
bool check_operation_rotate(void);
void fix_block(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position);

#endif /* BLOCK_H */
