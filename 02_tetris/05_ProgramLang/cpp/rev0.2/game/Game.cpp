#include <iostream>
#include <vector>
#include "../Settings.hpp"
#include "../block/Block.hpp"
#include "../board/Board.hpp"
#include "../collision/Collision.hpp"
#include "../input/Input.hpp"
#include "Game.hpp"

namespace game {

/* game.py では board.board から get_bingo_lines を import した後、
 * モジュール末尾で同名の get_bingo_lines() を再定義しているため、
 * power_on_game() 内ではこのローカル版(board側とロジックは同一)が使用される。
 * namespace game 内に同名で定義することで、この「上書き」を再現する。 */
static std::vector<int> get_bingo_lines();

static long collision_count = 0;
static long bingo_count = 0;
static long block_count = 0;
static long fix_count = 0;
static long rotate_count = 0;

void power_on_game()
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[task] power on" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    init_game();

    char put_key = '\0';
    const block::BlockShape *blk = &block::get_block();
    block_count++;
    int x = 3;
    int y = 0;
    double score = 0;
    int rotation = 0;
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    int proc_cnt = 0;
    char commands[6] = {
        settings::KEY_DROP,
        settings::KEY_LEFT,
        settings::KEY_RIGHT,
        settings::KEY_ROTATION_LEFT,
        settings::KEY_ROTATION_RIGHT,
        settings::KEY_HARD_DROP,
    };
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    while (put_key != settings::KEY_GAME_FINISH) {

        /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
        if (false) {
            if (settings::OS_ENVIROMENT == settings::LINUX) {
                put_key = input::getch_for_Linux();
            } else if (settings::OS_ENVIROMENT == settings::WINDOWS) {
#if defined(_WIN32)
                if (_kbhit()) {
                    put_key = static_cast<char>(_getch());
                }
#endif
            } else {
                put_key = static_cast<char>(std::cin.get());
            }
        } else {
            if (proc_cnt < 1000000) {
                put_key = commands[proc_cnt % 6];
                proc_cnt += 1;
            } else {
                break;              /* 10万回計測完了 */
            }
        }
        /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */

        rotation = input::request_operation_rotate(put_key, *blk, x, y, rotation);
        rotate_count++;
        /* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
        int next_x, next_y;
        input::get_next_position(put_key, *blk, x, y, rotation, next_x, next_y);
        /* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
        if (collision::is_invalid_position(*blk, next_x, next_y, rotation)) {
            next_x = x;
            next_y = y;
        }

        /* 衝突検知 */
        if (collision::check_collision_detection(*blk, next_x, next_y, rotation)) {
            collision_count++;
            block::fix_block(*blk, next_x, next_y, rotation);  /* update board result */
            fix_count++;
            // std::cout << "x=" << x << std::endl;
            // std::cout << "y=" << y << std::endl;
            // std::cout << "next_x=" << next_x << std::endl;
            // std::cout << "next_y=" << next_y << std::endl;

            /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
            // game over
            // if (is_game_over(put_key) == true) {
            //     std::cout << "game over!" << std::endl;
            //     break;
            // }
            /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */

            /* bingo */
            std::vector<int> bingo_lines = get_bingo_lines();
            /* ▼▼▼ 処理速度が影響していた処理を追加 ▼▼▼ */
            if (!bingo_lines.empty()) {
                bingo_count++;
            /* ▲▲▲ 処理速度が影響していた処理を追加 ▲▲▲ */
                /* ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼ */
                // score += bingo_lines.size();
                score += bingo_lines.size() * settings::SCORE_MULTIPLIER[bingo_lines.size()];
                /* ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲ */
                board::clear_bingo_lines();
            }

            blk = &block::get_block();
            block_count++;
            x = 3;
            y = 0;
            rotation = 0;
        } else {
            x = next_x;
            y = next_y;
        }

        // std::cout << rotation << std::endl;
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
        // board::update_view(*blk, x, y, rotation);
    }
    // std::cout << "score : " << score * 100 << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    // measurement_print();
}

/* initialize header
 * initialize functions
 */
void init_game()
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[init] initialize" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    board::init_board();
    block::create_blocks();
}

static std::vector<int> get_bingo_lines()
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

bool is_game_over(char put_key)
{
    int next_y;
    if (put_key == settings::KEY_DROP) {
        next_y = 1;
    } else {
        next_y = 0;
    }
    for (int c = 0; c < settings::BOARD_SIZE_WIDTH; ++c) {
        if (settings::board_result[next_y][c] == 1) {
            return true;
        }
    }
    return false;
}

void measurement_print()
{
    printf("collision = %ld\n", collision_count);
    printf("bingo     = %ld\n", bingo_count);
    printf("block     = %ld\n", block_count);
    printf("fix       = %ld\n", fix_count);
    printf("rotate    = %ld\n", rotate_count);
}

} // namespace game
