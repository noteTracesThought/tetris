#ifndef GAME_HPP
#define GAME_HPP

namespace game {

/* tetris main task header
 * tetris main task functions
 *
 * Todo:
 *     * 側面衝突検知時は壁扱いとなるように修正すること
 *     * ブロックが側面の壁に到達しない
 *     * 周期タスク処理
 */
void power_on_game();

/* initialize header
 * initialize functions
 */
void init_game();

bool is_game_over(char put_key);

} // namespace game

#endif // GAME_HPP
