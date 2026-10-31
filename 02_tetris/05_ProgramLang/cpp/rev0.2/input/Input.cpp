/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
#include "../Settings.hpp"
#include "../block/Block.hpp"
#include "../collision/Collision.hpp"
#include "Input.hpp"
/* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */

#if defined(__linux__)
#include <cstdio>
#include <unistd.h>
#include <termios.h>
#elif defined(_WIN32)
#include <conio.h>
#else
// Do Nothing
#endif

namespace input {

int request_operation_rotate(char put_key, const block::BlockShape &blk, int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[req] request_operation_rotate" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    if (put_key == settings::KEY_ROTATION_LEFT) {
        rotation = request_operation_rotate_left(blk, x, y, rotation);
    }
    if (put_key == settings::KEY_ROTATION_RIGHT) {
        rotation = request_operation_rotate_right(blk, x, y, rotation);
    }
    return rotation;
}

/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
void get_next_position(char put_key, const block::BlockShape &blk, int x, int y, int rotation, int &next_x, int &next_y)
{
    /* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[req] get_next_position" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */

    next_x = x;
    next_y = y;
    if (put_key == settings::KEY_RIGHT) {
        next_x += 1;
    } else if (put_key == settings::KEY_LEFT) {
        next_x -= 1;
    } else if (put_key == settings::KEY_DROP) {
        next_y += 1;
    /* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
    } else if (put_key == settings::KEY_HARD_DROP) {
        next_y = collision::execute_hard_drop(blk, x, y, rotation);
    /* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
    } else {
        // Do Nothing
    }
}

int request_operation_rotate_left(const block::BlockShape &blk, int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[req] request_operation_rotate_left" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int new_rotation = rotation - 1;
    if (new_rotation < 0) {
        new_rotation = 3;
    }

    int block_width = block::get_block_width(blk, new_rotation);
    int block_height = block::get_block_height(blk, new_rotation);
    if (x + block_width < 0) {
        new_rotation = rotation;
    }
    if (x + block_width > settings::BOARD_SIZE_WIDTH) {
        new_rotation = rotation;
    }
    if (y + block_height < 0) {
        new_rotation = rotation;
    }
    if (y + block_height > settings::BOARD_SIZE_HEIGHT) {
        new_rotation = rotation;
    }

    return new_rotation;
}

int request_operation_rotate_right(const block::BlockShape &blk, int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[req] request_operation_rotate_right" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int new_rotation = rotation + 1;
    new_rotation = new_rotation % 4;

    int block_width = block::get_block_width(blk, new_rotation);
    int block_height = block::get_block_height(blk, new_rotation);
    if (x + block_width < 0) {
        new_rotation = rotation;
    }
    if (x + block_width >= settings::BOARD_SIZE_WIDTH) {
        new_rotation = rotation;
    }
    if (y + block_height < 0) {
        new_rotation = rotation;
    }
    if (y + block_height >= settings::BOARD_SIZE_HEIGHT) {
        new_rotation = rotation;
    }

    return new_rotation;
}

char getch_for_Linux()
{
#if defined(__linux__)
    struct termios old_termios{}, raw_termios{};
    char ch;

    tcgetattr(STDIN_FILENO, &old_termios);
    raw_termios = old_termios;
    raw_termios.c_lflag &= ~(ICANON | ECHO);
    raw_termios.c_cc[VMIN] = 1;
    raw_termios.c_cc[VTIME] = 0;

    tcsetattr(STDIN_FILENO, TCSANOW, &raw_termios);
    ch = static_cast<char>(getchar());
    tcsetattr(STDIN_FILENO, TCSADRAIN, &old_termios);

    return ch;
#else
    // Linux以外の環境では未使用
    return '\0';
#endif
}

} // namespace input
