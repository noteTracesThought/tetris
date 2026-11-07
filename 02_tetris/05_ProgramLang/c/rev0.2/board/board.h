#ifndef BOARD_H
#define BOARD_H

#include "../settings.h"

/* get_bingo_lines() の戻り値 (Pythonのlistに相当) */
typedef struct {
    int rows[BOARD_SIZE_HEIGHT];
    int count;
} bingo_lines_t;

void update_view(const int block[4][4][4], int x, int y, int rotation);
void init_board(void);
void create_board(void);
void load_board_result(void);
void draw_board(int board_param[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH]);
void clear_bingo_lines(void);
bingo_lines_t get_bingo_lines(void);

#endif /* BOARD_H */
