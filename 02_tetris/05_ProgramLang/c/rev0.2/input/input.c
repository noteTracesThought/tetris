/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
#include <string.h>
#include "../settings.h"
#include "../block/block.h"
#include "../collision/collision.h"
#include "input.h"
/* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */

#if defined(__linux__)
#include <stdio.h>
#include <unistd.h>
#include <termios.h>
#elif defined(_WIN32)
#include <conio.h>
#else
/* Do Nothing */
#endif

int request_operation_rotate(char put_key, const int block[4][4][4], int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[req] request_operation_rotate\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    if (put_key == KEY_ROTATION_LEFT) {
        rotation = request_operation_rotate_left(block, x, y, rotation);
    }
    if (put_key == KEY_ROTATION_RIGHT) {
        rotation = request_operation_rotate_right(block, x, y, rotation);
    }
    return rotation;
}

/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
void get_next_position(char put_key, const int block[4][4][4], int x, int y, int rotation, int *next_x, int *next_y)
{
    /* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[req] get_next_position\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */

    *next_x = x;
    *next_y = y;
    if (put_key == KEY_RIGHT) {
        *next_x += 1;
    } else if (put_key == KEY_LEFT) {
        *next_x -= 1;
    } else if (put_key == KEY_DROP) {
        *next_y += 1;
    /* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
    } else if (put_key == KEY_HARD_DROP) {
        *next_y = execute_hard_drop(block, x, y, rotation);
    /* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
    } else {
        /* Do Nothing */
    }
}

int request_operation_rotate_left(const int block[4][4][4], int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[req] request_operation_rotate_left\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int new_rotation = rotation - 1;
    if (new_rotation < 0) {
        new_rotation = 3;
    }

    int block_width = get_block_width(block, new_rotation);
    int block_height = get_block_height(block, new_rotation);
    if (x + block_width < 0) {
        /* printf("x + block_width:%d\n", x + block_width); */
        new_rotation = rotation;
    }
    if (x + block_width > BOARD_SIZE_WIDTH) {
        /* printf("x + block_width:%d\n", x + block_width); */
        new_rotation = rotation;
    }
    if (y + block_height < 0) {
        /* printf("x + block_width:%d\n", y + block_height); */
        new_rotation = rotation;
    }
    if (y + block_height > BOARD_SIZE_HEIGHT) {
        /* printf("x + block_width:%d\n", y + block_height); */
        new_rotation = rotation;
    }

    return new_rotation;
}

int request_operation_rotate_right(const int block[4][4][4], int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    /* printf("[req] request_operation_rotate_right\n"); */
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int new_rotation = rotation + 1;
    new_rotation = new_rotation % 4;

    int block_width = get_block_width(block, new_rotation);
    int block_height = get_block_height(block, new_rotation);
    if (x + block_width < 0) {
        /* printf("x + block_width:%d\n", x + block_width); */
        new_rotation = rotation;
    }
    if (x + block_width >= BOARD_SIZE_WIDTH) {
        /* printf("x + block_width:%d\n", x + block_width); */
        new_rotation = rotation;
    }
    if (y + block_height < 0) {
        /* printf("x + block_width:%d\n", y + block_height); */
        new_rotation = rotation;
    }
    if (y + block_height >= BOARD_SIZE_HEIGHT) {
        /* printf("x + block_width:%d\n", y + block_height); */
        new_rotation = rotation;
    }

    return new_rotation;
}

char getch_for_Linux(void)
{
#if defined(__linux__)
    struct termios old_termios, raw_termios;
    char ch;

    tcgetattr(STDIN_FILENO, &old_termios);
    raw_termios = old_termios;
    raw_termios.c_lflag &= ~(ICANON | ECHO);
    raw_termios.c_cc[VMIN] = 1;
    raw_termios.c_cc[VTIME] = 0;

    tcsetattr(STDIN_FILENO, TCSANOW, &raw_termios);
    ch = (char)getchar();
    tcsetattr(STDIN_FILENO, TCSADRAIN, &old_termios);

    return ch;
#else
    /* Linux以外の環境では未使用 */
    return '\0';
#endif
}
