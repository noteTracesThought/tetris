#ifndef BOARD_HPP
#define BOARD_HPP

#include "../Settings.hpp"
#include "../block/Block.hpp"

namespace board {

/* get_bingo_lines() の戻り値 (Pythonのlistに相当、通常の固定長配列で実装) */
struct BingoLines {
    int rows[settings::BOARD_SIZE_HEIGHT];
    int count;
};

void update_view(const int block[4][4][4], int x, int y, int rotation);
void init_board();
void create_board();
void load_board_result();
void draw_board(int board_param[settings::BOARD_SIZE_HEIGHT][settings::BOARD_SIZE_WIDTH]);
void clear_bingo_lines();
BingoLines get_bingo_lines();

} // namespace board

#endif // BOARD_HPP
