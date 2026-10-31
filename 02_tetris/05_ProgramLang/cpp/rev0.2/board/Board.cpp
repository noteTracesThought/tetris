#include <iostream>
#include "../board/Board.hpp"

namespace board {

void update_view(const block::BlockShape &block, int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[view] update_view" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */

    // view
    load_board_result();                   /* おばけ(残像)を消す */
    for (std::size_t r = 0; r < block[rotation].size(); ++r) {
        for (std::size_t c = 0; c < block[rotation][r].size(); ++c) {
            if (block[rotation][r][c] == 1) {
                settings::board[y + r][x + c] = 1;
                // std::cout << "r+y: " << r + y << std::endl;
                // std::cout << "c+x: " << c + x << std::endl;
            }
        }
    }
    draw_board(settings::board);
}

/* board header
 * group board functions
 */
void init_board()
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[init] init_board" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    create_board();
}

void create_board()
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[init] create_board" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    for (auto &row : settings::board_result) {
        row.fill(0);
    }
    for (auto &row : settings::board) {
        row.fill(0);
    }
}

void load_board_result()
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[init] load_board_result" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    settings::board = settings::board_result;
}

void draw_board(const settings::BoardArray &board_param)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[proc] draw_board" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    for (const auto &row : board_param) {
        std::string line;
        for (int cell : row) {
            if (cell == 0) {
                line += "\xE2\x96\xA1"; // □
            } else {
                line += "\xE2\x96\xA0"; // ■
            }
        }
        std::cout << line << std::endl;
    }
}

void clear_bingo_lines()
{
    settings::BoardArray new_board{};
    int new_board_count = 0;

    for (const auto &row : settings::board_result) {
        int ones = 0;
        for (int cell : row) {
            if (cell == 1) {
                ones++;
            }
        }
        if (ones < settings::BOARD_SIZE_WIDTH) {
            new_board[new_board_count] = row;
            new_board_count++;
        }
    }

    while (new_board_count < settings::BOARD_SIZE_HEIGHT) {
        /* new_board.insert(0, [0]*BOARD_SIZE_WIDTH) 相当 */
        for (int r = new_board_count; r > 0; r--) {
            new_board[r] = new_board[r - 1];
        }
        new_board[0].fill(0);
        new_board_count++;
    }

    settings::board_result = new_board;
}

std::vector<int> get_bingo_lines()
{
    std::vector<int> delete_rows;

    for (std::size_t r = 0; r < settings::board_result.size(); ++r) {
        for (std::size_t c = 0; c < settings::board_result[r].size(); ++c) {
            if (settings::board_result[r][c] != 1) {
                break;
            }
            if (static_cast<int>(c) >= settings::BOARD_SIZE_WIDTH - 1) {
                delete_rows.push_back(static_cast<int>(r));
                std::cout << "bingo!!" << std::endl;
            }
        }
    }
    return delete_rows;
}

} // namespace board
