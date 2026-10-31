#ifndef COLLISION_HPP
#define COLLISION_HPP

#include "../block/Block.hpp"

namespace collision {

/* update check header
 * update check functions
 *
 * Todo:
 *     * rotate
 */
bool is_invalid_position(const block::BlockShape &block, int x, int y, int rotation);
bool is_out_of_board(const block::BlockShape &block, int x, int y, int rotation);
bool check_collision_detection(const block::BlockShape &block, int next_x, int next_y, int rotation);
/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
int execute_hard_drop(const block::BlockShape &block, int x, int y, int rotation);
/* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */

} // namespace collision

#endif // COLLISION_HPP
