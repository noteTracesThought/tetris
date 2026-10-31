#include <iostream>
#include <chrono>
#include "game/Game.hpp"

/* tetris main task header
 * tetris main task functions
 *
 * Todo:
 *     * 側面衝突検知時は壁扱いとなるように修正すること
 *     * ブロックが側面の壁に到達しない
 *     * 周期タスク処理
 */

int main()
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    auto start = std::chrono::steady_clock::now();
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    game::power_on_game();
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    auto stop = std::chrono::steady_clock::now();
    double elapsed_ms = std::chrono::duration<double, std::milli>(stop - start).count();
    std::cout << "time = " << elapsed_ms << "ms" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    std::cout << "[task] power off" << std::endl;

    return 0;
}
