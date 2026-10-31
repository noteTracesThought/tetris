#ifndef COLLISION_H
#define COLLISION_H

#include <stdbool.h>

/* update check header
 * update check functions
 *
 * Todo:
 *     * rotate
 */
bool is_invalid_position(const int block[4][4][4], int x, int y, int rotation);
bool is_out_of_board(const int block[4][4][4], int x, int y, int rotation);
bool check_collision_detection(const int block[4][4][4], int next_x, int next_y, int rotation);
/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
int execute_hard_drop(const int block[4][4][4], int x, int y, int rotation);
/* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */

#endif /* COLLISION_H */
