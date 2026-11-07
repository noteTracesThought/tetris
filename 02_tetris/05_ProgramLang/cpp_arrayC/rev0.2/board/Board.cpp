#include <iostream>
#include <cstring>
#include "../board/Board.hpp"

namespace board {

void update_view(const int block[4][4][4], int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[view] update_view" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */

    // view
    load_board_result();                   /* おばけ(残像)を消す */
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < 4; c++) {
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
    for (int r = 0; r < settings::BOARD_SIZE_HEIGHT; r++) {
        for (int c = 0; c < settings::BOARD_SIZE_WIDTH; c++) {
            settings::board_result[r][c] = 0;
            settings::board[r][c] = 0;
        }
    }
}

void load_board_result()
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[init] load_board_result" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    for (int r = 0; r < settings::BOARD_SIZE_HEIGHT; r++) {
        std::memcpy(settings::board[r], settings::board_result[r], sizeof(int) * settings::BOARD_SIZE_WIDTH);
    }
}

void draw_board(int board_param[settings::BOARD_SIZE_HEIGHT][settings::BOARD_SIZE_WIDTH])
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[proc] draw_board" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    for (int r = 0; r < settings::BOARD_SIZE_HEIGHT; r++) {
        std::string line;
        for (int c = 0; c < settings::BOARD_SIZE_WIDTH; c++) {
            if (board_param[r][c] == 0) {
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
    int new_board[settings::BOARD_SIZE_HEIGHT][settings::BOARD_SIZE_WIDTH];
    int new_board_count = 0;

    for (int r = 0; r < settings::BOARD_SIZE_HEIGHT; r++) {
        int ones = 0;
        for (int c = 0; c < settings::BOARD_SIZE_WIDTH; c++) {
            if (settings::board_result[r][c] == 1) {
                ones++;
            }
        }
        if (ones < settings::BOARD_SIZE_WIDTH) {
            std::memcpy(new_board[new_board_count], settings::board_result[r], sizeof(int) * settings::BOARD_SIZE_WIDTH);
            new_board_count++;
        }
    }

    while (new_board_count < settings::BOARD_SIZE_HEIGHT) {
        /* new_board.insert(0, [0]*BOARD_SIZE_WIDTH) 相当 */
        for (int r = new_board_count; r > 0; r--) {
            std::memcpy(new_board[r], new_board[r - 1], sizeof(int) * settings::BOARD_SIZE_WIDTH);
        }
        for (int c = 0; c < settings::BOARD_SIZE_WIDTH; c++) {
            new_board[0][c] = 0;
        }
        new_board_count++;
    }

    for (int r = 0; r < settings::BOARD_SIZE_HEIGHT; r++) {
        std::memcpy(settings::board_result[r], new_board[r], sizeof(int) * settings::BOARD_SIZE_WIDTH);
    }
}

bingo_lines_t get_bingo_lines()
{
    bingo_lines_t delete_rows;
    delete_rows.count = 0;

    for (int r = 0; r < settings::BOARD_SIZE_HEIGHT; r++) {
        for (int c = 0; c < settings::BOARD_SIZE_WIDTH; c++) {
            if (settings::board_result[r][c] != 1) {
                break;
            }
            if (c >= settings::BOARD_SIZE_WIDTH - 1) {
                delete_rows.rows[delete_rows.count++] = r;
                std::cout << "bingo!!" << std::endl;
            }
        }
    }
    return delete_rows;
}

} // namespace board
