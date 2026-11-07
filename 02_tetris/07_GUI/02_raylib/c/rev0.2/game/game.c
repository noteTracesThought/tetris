#include <stdio.h>
#include <time.h>
#include "../settings.h"
#include "../collision/collision.h"
#include "../input/input.h"
#include "../cycle/cycle.h"
#include "../cycle/cycle_process.h"
#include "game.h"

#if defined(__linux__)
/* Do Nothing (input.c 側でインクルード済み) */
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
// const double CPU_SLEEP  = 0.01;         /* 10ms */
#define CPU_SLEEP           0.01         /* 10ms */

/*----------------------------*/
/* variable */
/*----------------------------*/
static bool is_update          = false;
static long collision_count    = 0;
static long bingo_count        = 0;
static long block_count        = 0;
static long fix_count          = 0;
static long rotate_count       = 0;

/*----------------------------*/
/* function section */
/*----------------------------*/

/*----------------------------*/
/* public function */
/*----------------------------*/
void power_on_game(void)
{
    /* printf("[task] power on\n"); */
    init_game();
    init_input();
    cycle_init();

    char put_key = '\0';
    common_pos_t current = { .x = 3, .y = 0, .rotation = 0 };
    double score = 0;
    int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH];

    get_block(block, current);
    set_update_view(false);
    while (put_key != KEY_GAME_FINISH)
    {
        input_putkey();
        cycle_mainloop();
        cycle_process_run();
        time_sleep(CPU_SLEEP);

        put_key = '\0';                 /* Pythonの None 相当 */
        char _put_key = get_putkey();
        if (_put_key)
        {
            put_key = _put_key;
        }

        common_pos_t next = current;
        request_operation_rotate(put_key, &next);
        get_next_position(put_key, block, &next);

        /* 既存ブロック衝突、ボード側面衝突検知 */
        if (adjust_pos(block, &next) == false)
        {
            next = current;
        }

        /* 落下衝突検知 */
        if (check_fall_collision(block, next) == true)
        {
            fix_block(block, next);  /* update board result */

            /* game over */
            if (is_game_over(put_key) == true)
            {
                printf("game over!\n");
                break;
            }

            /* bingo */
            bingo_lines_t bingo_lines = get_bingo_lines();
            if (bingo_lines.count > 0)
            {
                printf("bingo!!\n");
            }
            score += bingo_lines.count * SCORE_MULTIPLIER[bingo_lines.count];
            clear_bingo_lines();

            get_block(block, current);
            current = (common_pos_t){ .x = 3, .y = 0, .rotation = 0 };
        }
        else
        {
            current = next;
        }

        /* 落下イベントが発生した場合、ブロックを1マス落下させる */
        if (pop_fall_event() == true)
        {
            set_update_view(true);
            current.y += 1;
        }
        is_update_view(block, current);
    }

    printf("score : %d\n", (int)(score * 100));
    restore_input();
}

/* initialize header
 * initialize functions
 */
void init_game(void)
{
    /* printf("[init] initialize\n"); */
    init_board();
    create_blocks();
}

bool is_game_over(char put_key)
{
    int board_y = put_key == KEY_DROP ? 1 : 0;
    int board_result[BOARD_HEIGHT][BOARD_WIDTH];
    get_board_boardresult(board_result);

    for (int c = 0; c < BOARD_SIZE_WIDTH; c++)
    {
        if (board_result[board_y][c] == 1)
        {
            return true;
        }
    }
    return false;
}

void set_update_view(bool value)
{
    is_update = value;
}

void is_update_view(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    if (is_update == true)
    {
        update_view(block, position);
        set_update_view(false);
    }
}


void is_update_view_gui(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position)
{
    if (is_update == true)
    {
        update_view(block, position);
        set_update_view(false);
    }
}

/* Pythonの time.sleep() 相当 */
void time_sleep(double seconds)
{
#if defined(_WIN32)
    Sleep((DWORD)(seconds * 1000));
#else
    struct timespec ts;
    ts.tv_sec = (time_t)seconds;
    ts.tv_nsec = (long)((seconds - (double)ts.tv_sec) * 1000000000.0);
    nanosleep(&ts, NULL);
#endif
}

/*----------------------------*/
/* private function */
/*----------------------------*/
