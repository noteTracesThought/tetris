#include "../collision/Collision.hpp"
#include "../Settings.hpp"

namespace collision {

bool is_invalid_position(const block::BlockShape &blk, int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[check] is_invalid_position" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    bool is_invalid = false;
    bool is_invalid_move = is_out_of_board(blk, x, y, rotation);
    bool is_invalid_rotate = block::check_operation_rotate();
    if (is_invalid_move || is_invalid_rotate) {
        is_invalid = true;
    }
    return is_invalid;
}

bool is_out_of_board(const block::BlockShape &blk, int x, int y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[check] is_out_of_board" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    bool is_invalid = false;
    int block_width = block::get_block_width(blk, rotation);
    int block_height = block::get_block_height(blk, rotation);
    if (x < 0) {
        is_invalid = true;
    }
    if (y < 0) {
        is_invalid = true;
    }
    if (x > settings::BOARD_SIZE_WIDTH - block_width) {
        is_invalid = true;
    }
    if (y > settings::BOARD_SIZE_HEIGHT - block_height) {
        is_invalid = true;
    }
    return is_invalid;
}

bool check_collision_detection(const block::BlockShape &blk, int next_x, int next_y, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[check] check_collision_detection" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int block_height = block::get_block_height(blk, rotation);

    for (std::size_t r = 0; r < blk[rotation].size(); ++r) {
        for (std::size_t c = 0; c < blk[rotation][r].size(); ++c) {
            /* 衝突検知(床) */
            if (next_y >= settings::BOARD_SIZE_HEIGHT - block_height) {
                // std::cout << "next_y:" << next_y << std::endl;
                return true;
            }

            /* next(blockなし) */
            if (blk[rotation][r][c] != 1) {
                continue;
            }

            /* 衝突検知(board block) */
            if (settings::board_result[next_y + r][next_x + c] == 1) {
                // std::cout << "next_y+r:" << next_y + r << std::endl;
                // std::cout << "next_x+c:" << next_x + c << std::endl;
                return true;
            }

            /* 衝突検知(next board block) */
            if (settings::board_result[next_y + r + 1][next_x + c] == 1) {
                // std::cout << "next_y+r+1:" << next_y + r + 1 << std::endl;
                // std::cout << "next_x+c:" << next_x + c << std::endl;
                return true;
            }
        }
    }

    return false;
}

/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
int execute_hard_drop(const block::BlockShape &blk, int x, int y, int rotation)
{
    /* ハードドロップを実行する */
    int current_y = y;
    int next_y = y;

    for (;;) {
        /* 仮想的に1段下の位置（Position）を計算して next にセットするだけ
         * (Python版のtry/exceptは実質到達しないため、単純なループとして実装)
         */
        next_y += 1;

        /* その1段下（next）で衝突するかチェック */
        if (check_collision_detection(blk, x, next_y, rotation)) {
            /* ぶつかるなら、今の current（衝突する直前の安全な位置）が最終位置なので終了 */
            break;
        }

        /* ぶつからなければ、現在位置(current)を1段下に進めて次のループへ */
        current_y = next_y;
    }
    next_y = current_y;

    return next_y;
}
/* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */

} // namespace collision
