#ifndef BOARD_HPP
#define BOARD_HPP

#include <vector>
#include "../Settings.hpp"
#include "../block/Block.hpp"

namespace board {

void update_view(const block::BlockShape &block, int x, int y, int rotation);
void init_board();
void create_board();
void load_board_result();
void draw_board(const settings::BoardArray &board_param);
void clear_bingo_lines();
std::vector<int> get_bingo_lines();

} // namespace board

#endif // BOARD_HPP
