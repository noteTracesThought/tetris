#include <string.h>
#include "../settings.h"
#include "../collision/collision.h"
#include "input.h"

#if defined(__linux__)
#include <stdio.h>
#include <unistd.h>
#include <sys/select.h>
#include <termios.h>
#elif defined(_WIN32)
#include <conio.h>
#else
/* Do Nothing */
#endif

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/

/*----------------------------*/
/* variable */
/*----------------------------*/
static struct termios _old_settings;
static char settings_put_key = '\0';
static int _settings_saved = 0; // 設定が保存されているかのフラグ

/*----------------------------*/
/* function section */
/*----------------------------*/
char get_key_non_blocking(void);

/*----------------------------*/
/* public function */
/*----------------------------*/
void init_input(void)
{
    /* """プログラム開始時にターミナル設定を保存""" */
    #if defined(__linux__)
    if (!_settings_saved)
    {
        int fd = fileno(stdin);
        tcgetattr(fd, &_old_settings);
        _settings_saved = 1;
    }
    #endif
}

void request_operation_rotate(char put_key, common_pos_t *position)
{
    /* printf("[req] request_operation_rotate\n"); */
    if (put_key == KEY_ROTATION_LEFT)
    {
        position->rotation = (position->rotation + 3) % 4;
    }
    else if (put_key == KEY_ROTATION_RIGHT)
    {
        position->rotation = (position->rotation + 1) % 4;
    }
}

void get_next_position(char put_key, const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t *position)
{
    /* printf("[req] get_next_position\n"); */
    if (put_key == KEY_RIGHT)
    {
        position->x += 1;
    }
    else if (put_key == KEY_LEFT)
    {
        position->x -= 1;
    }
    else if (put_key == KEY_DROP)
    {
        position->y += 1;
    }
    else if (put_key == KEY_HARD_DROP)
    {
        *position = execute_hard_drop(block, *position);
    }
    else
    {
        /* Do Nothing */
    }
}

void input_putkey(void)
{
    char put_key;
    /* 毎ミリ秒（メインループ）で呼び出す */
    put_key = get_key_non_blocking();
    // if(put_key != NULL)
    if(put_key != '\0')
    {
        settings_put_key = put_key;
    }
}

void set_putkey(char value)
{
    settings_put_key = value;
}

char get_putkey(void)
{
    char result;
    result = settings_put_key;
    settings_put_key = '\0';  /* クリア */
    return result;
}

void restore_input(void)
{
    /* """プログラム終了時にターミナル設定を元に戻す""" */
    #ifdef __linux__
    if (_settings_saved)
    {
        int fd = fileno(stdin);
        tcsetattr(fd, TCSADRAIN, &_old_settings);
    }
    #endif
}

/*----------------------------*/
/* private function */
/*----------------------------*/
char get_key_non_blocking(void)
{
#if defined(__linux__)
    struct termios old_termios, raw_termios;
    fd_set readfds;
    struct timeval timeout;
    int ch;

    if (tcgetattr(STDIN_FILENO, &old_termios) == -1)
    {
        return '\0';
    }

    raw_termios = old_termios;
    raw_termios.c_lflag &= ~(ICANON | ECHO);
    raw_termios.c_cc[VMIN] = 1;
    raw_termios.c_cc[VTIME] = 0;

    if (tcsetattr(STDIN_FILENO, TCSANOW, &raw_termios) == -1)
    {
        return '\0';
    }

    FD_ZERO(&readfds);
    FD_SET(STDIN_FILENO, &readfds);

    timeout.tv_sec = 0;
    timeout.tv_usec = 0;

    if (select(STDIN_FILENO + 1, &readfds, NULL, NULL, &timeout) > 0)
    {
        ch = getchar();
    }
    else
    {
        ch = '\0';
    }

    tcsetattr(STDIN_FILENO, TCSADRAIN, &old_termios);

    if (ch == EOF)
    {
        clearerr(stdin);
        return '\0';
    }

    return (char)ch;
#else
    return '\0';
#endif
}