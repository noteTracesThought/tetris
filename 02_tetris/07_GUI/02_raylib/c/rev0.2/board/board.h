#ifndef BOARD_H
#define BOARD_H

#include "../settings.h"
#include "../common/common.h"
#include "../block/block.h"

/*----------------------------*/
/* type */
/*----------------------------*/
/* get_bingo_lines() の戻り値 (Pythonのlistに相当) */
typedef struct
{
    int rows[BOARD_SIZE_HEIGHT];
    int count;
} bingo_lines_t;

enum {
    BOARD_CELL_EMPTY = 0,       /* Blockなし */
    BOARD_CELL_OCCUPIED = 1     /* Blockあり */
};

/*----------------------------*/
/* const */
/*----------------------------*/
#define BOARD_HEIGHT BOARD_SIZE_HEIGHT   /* board height */
#define BOARD_WIDTH  BOARD_SIZE_WIDTH   /* board width */

/*----------------------------*/
/* variable */
/*----------------------------*/

/*----------------------------*/
/* function section */
/*----------------------------*/

/*----------------------------*/
/* public function */
/*----------------------------*/
void update_view(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position);
void init_board(void);
void create_board(void);
void load_board_result(void);
void draw_board(int board_param[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH]);
void clear_bingo_lines(void);
bingo_lines_t get_bingo_lines(void);

/* 永続状態 */
void set_board_boardresult(const int value[BOARD_HEIGHT][BOARD_WIDTH]);
void get_board_boardresult(int value[BOARD_HEIGHT][BOARD_WIDTH]);
/* 描画用 */
void set_board_boardview(const int value[BOARD_HEIGHT][BOARD_WIDTH]);
void get_board_boardview(int value[BOARD_HEIGHT][BOARD_WIDTH]);

#endif /* BOARD_H */
