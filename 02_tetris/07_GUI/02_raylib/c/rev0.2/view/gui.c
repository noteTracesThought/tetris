#include <stdio.h>
#include <time.h>

#include "raylib.h"
#include "../settings.h"
#include "../common/common.h"
#include "../block/block.h"
#include "../board/board.h"
#include "../collision/collision.h"
#include "../input/input.h"
#include "../cycle/cycle.h"
#include "../cycle/cycle_process.h"
#include "../game/game.h"
#include "../view/gui.h"

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
typedef struct
{
    int         state_number;
    const char *state_name;
} gui_game_state_t;

typedef struct
{
    const int  key_src;
    const char key_dest;
} gui_key_map_t;

enum game_state_number
{
    STATE_INIT  = 0,
    STATE_INPUT = 1,
    STATE_LOGIC = 2,
    STATE_VIEW  = 3,
    STATE_QUIT  = 4,
    STATE_MAX
};

typedef enum
{
    LOGIC_CONTINUE,
    LOGIC_GAME_OVER
} gui_logic_result_t;

/*----------------------------*/
/* const */
/*----------------------------*/
#define TITLE               "tetris"
#define FRAME_WIDTH         400
#define FRAME_HEIGHT        600
#define CELL_SIZE           FRAME_HEIGHT / 20
#define BOARD_X             FRAME_WIDTH / 20 * 2
#define BOARD_Y             0
#define CPU_SLEEP           0.01         /* 10ms */

/* STATE TYPE(debug用) */
#define INIT_TYPE           "INIT"
#define INPUT_TYPE          "INPUT"
#define LOGIC_TYPE          "LOGIC"
#define VIEW_TYPE           "VIEW"
#define QUIT_TYPE           "QUIT"

static const gui_game_state_t GAME_STATE[]  =
{
    /* state_number,   state_name(debug用) */
    {STATE_INIT,       INIT_TYPE},
    {STATE_INPUT,      INPUT_TYPE},
    {STATE_LOGIC,      LOGIC_TYPE},
    {STATE_VIEW,       VIEW_TYPE},
    {STATE_QUIT,       QUIT_TYPE}
};

/* 1. pyrayのキーとゲーム内キーのマッピング辞書を定義 */
static const gui_key_map_t KEY_MAP[] =
{
    /* key_src,        key_dest */
    {KEY_S,            KEY_LEFT},
    {KEY_D,            KEY_RIGHT},
    {KEY_R,            KEY_ROTATION_RIGHT},
    {KEY_W,            KEY_ROTATION_LEFT},
    {KEY_SPACE,        KEY_DROP},
    {KEY_H,            KEY_HARD_DROP},
    {KEY_Q,            KEY_GAME_FINISH}
};

/*----------------------------*/
/* variable */
/*----------------------------*/
static int game_state_now      = STATE_INIT;

/*----------------------------*/
/* function section */
/*----------------------------*/
void gui_init(void);
void draw_board_pyray(void);
void draw_current_block(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t current);
void draw_game(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t current);
void input_key_pyray(void);

void gui_state_init(int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t current);
void gui_state_input(char *put_key);
gui_logic_result_t gui_state_logic(int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t *current, char *put_key, double *score);

/*----------------------------*/
/* public function */
/*----------------------------*/
void gui_start(void)
{
    /* printf("[task] power on") */
    game_state_now = STATE_INIT;
    if(GAME_STATE[game_state_now].state_number == STATE_INIT)
    {
        common_pos_t  current = { .x = 3, .y = 0, .rotation = 0 };
        int             block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH];
        char            put_key = '\0';
        double          score = 0;

        gui_state_init(block,current);
        game_state_now = STATE_INPUT;
        /* メインループ */
        while (!WindowShouldClose()
             && GAME_STATE[game_state_now].state_number != STATE_QUIT) // ウィンドウの×ボタンが押されるまでループ
        {
            switch(GAME_STATE[game_state_now].state_number)
            {
                case STATE_INPUT:
                    /* ① pyrayから入力を取得 */
                    if (put_key == KEY_GAME_FINISH)
                    {
                        game_state_now = STATE_QUIT;
                        break;
                    }
                    gui_state_input(&put_key);
                    game_state_now = STATE_LOGIC;
                    break;

                case STATE_LOGIC:
                    /* ゲームロジック */
                    if (gui_state_logic(block, &current, &put_key, &score) == LOGIC_GAME_OVER)
                    {
                        game_state_now = STATE_QUIT;
                    }
                    else
                    {
                        game_state_now = STATE_VIEW;
                    }
                    break;

                case STATE_VIEW:
                    /* ④ pyrayで描画 */
                    draw_game(block, current);
                    game_state_now = STATE_INPUT;
                    break;

                case STATE_QUIT:
                    /* ゲーム終了 */
                    break;

                default:
                    /* Do Nothing */
                    game_state_now = STATE_INPUT;
                    break;
            }
        }

        if(GAME_STATE[game_state_now].state_number == STATE_QUIT)
        {
            /* ゲーム終了 */
            printf("%.0f\n", score * 100);
        }

        /* 3. 終了処理 */
        CloseWindow();
    }
}

/*----------------------------*/
/* private function */
/*----------------------------*/
void gui_init(void)
{
    /* 1. ウィンドウの初期化（幅800, 高さ450, タイトル） */
    InitWindow(FRAME_WIDTH, FRAME_HEIGHT, TITLE);

    /* フレームレートを60FPSに設定 */
    SetTargetFPS(60);
}

void draw_board_pyray(void)
{
    Color color;
    int board_result[BOARD_HEIGHT][BOARD_WIDTH];
    get_board_boardresult(board_result);

    for(int r = 0; r < BOARD_SIZE_HEIGHT; r++)
    {
        for(int c = 0; c < BOARD_SIZE_WIDTH; c++)
        {
            float px = BOARD_X + c * CELL_SIZE;
            float py = BOARD_Y + r * CELL_SIZE;

            if(board_result[r][c] == 1)
            {
                color = (Color){0, 200, 255, 255};    /* ボード上で確定しているブロック */
            }
            else
            {
                color = (Color){30, 30, 30, 255};     /* 背景の色 */
            }

            DrawRectangle(
                (int)px, (int)py, (int)CELL_SIZE, (int)CELL_SIZE,
                color
            );
        }
    }
}

/* 通常用 */
void draw_game(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t current)
{
    BeginDrawing();             /* 描画開始 */
    ClearBackground(BLACK); // 背景色を白にする
    draw_board_pyray();
    draw_current_block(block, current);
    EndDrawing();               /* 描画終了 */
}

void input_key_pyray(void)
{
    char put_key = '\0';
    for(int i = 0; i < KEY_MAX; i++)
    {
        if(IsKeyPressed(KEY_MAP[i].key_src) == true) /* 押しっぱなし防止 */
        {
            put_key = KEY_MAP[i].key_dest;
            break;   /* 1つ入力があったら抜ける */
        }
    }
    set_putkey(put_key);
}

void draw_current_block(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t current)
{
    const int (*current_block)[BLOCK_SIZE_WIDTH] = block[current.rotation];
    for(int r = 0; r < BLOCK_SIZE_HEIGHT; r++)
    {
        for(int c = 0; c < BLOCK_SIZE_WIDTH; c++)
        {
            if(current_block[r][c] != 1)
            {
                continue;
            }

            float px = BOARD_X + (current.x + c) * CELL_SIZE;
            float py = BOARD_Y + (current.y + r) * CELL_SIZE;

            DrawRectangle(
                (int)px, (int)py, (int)CELL_SIZE, (int)CELL_SIZE,
                (Color){255, 100, 100, 255}        /* 落下中のブロック */
            );
        }
    }
}

void gui_state_init(int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t current)
{
    init_game();
    init_input();
    cycle_init();
    gui_init();
    get_block(block, current);
    set_update_view(false);
}

void gui_state_input(char *put_key)
{
    /* ① pyrayから入力を取得 */
    input_key_pyray();
    *put_key = get_putkey();
}

gui_logic_result_t gui_state_logic(int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t *current, char *put_key, double *score)
{
    gui_logic_result_t logic_result = LOGIC_CONTINUE; /* デフォルトは継続処理 */

    /* ゲームロジック */
    /* 定期処理 */
    cycle_mainloop();
    cycle_process_run();
    time_sleep(CPU_SLEEP);

    bool fall_event = pop_fall_event();
    update_view_gui(block, *current);

    /* 操作処理 */
    common_pos_t next = *current;
    if (fall_event)
    {
        next.y += 1;
    }
    request_operation_rotate(*put_key, &next);
    get_next_position(*put_key, block, &next);

    /* 既存ブロック衝突、ボード側面衝突検知 */
    if (adjust_pos(block, &next) == false)
    {
        next = *current;
    }

    /* 落下衝突検知 */
    if (check_fall_collision(block, next) == true)
    {
        common_pos_t fix_position = check_move_collision(block, next) ? *current : next;
        fix_block(block, fix_position);

        /* game over */
        if (is_game_over(*put_key) == true)
        {
            printf("game over!\n");
            logic_result = LOGIC_GAME_OVER;
        }
        else
        {
            /* bingo */
            bingo_lines_t bingo_lines = get_bingo_lines();
            if (bingo_lines.count > 0)
            {
                printf("bingo!!\n");
            }
            *score += bingo_lines.count * SCORE_MULTIPLIER[bingo_lines.count];
            clear_bingo_lines();

            get_block(block, *current);
            *current = (common_pos_t){ .x = 3, .y = 0, .rotation = 0 };
        }
    }
    else
    {
        *current = next;
    }
    return logic_result;
}
