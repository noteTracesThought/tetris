#ifndef GAME_H
#define GAME_H

#include <stdbool.h>

/* tetris main task header
 * tetris main task functions
 *
 * Todo:
 *     * 側面衝突検知時は壁扱いとなるように修正すること
 *     * ブロックが側面の壁に到達しない
 *     * 周期タスク処理
 */
void power_on_game(void);

/* initialize header
 * initialize functions
 */
void init_game(void);

bool is_game_over(char put_key);

void measurement_print(void);

#endif /* GAME_H */
