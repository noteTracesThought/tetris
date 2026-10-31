#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <time.h>
#include "game/game.h"

/* tetris main task header
 * tetris main task functions
 *
 * Todo:
 *     * 側面衝突検知時は壁扱いとなるように修正すること
 *     * ブロックが側面の壁に到達しない
 *     * 周期タスク処理
 */

int main(void)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    struct timespec start, stop;
    clock_gettime(CLOCK_MONOTONIC, &start);
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    power_on_game();
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    clock_gettime(CLOCK_MONOTONIC, &stop);
    double elapsed_ms = (stop.tv_sec - start.tv_sec) * 1000.0
                       + (stop.tv_nsec - start.tv_nsec) / 1000000.0;
    printf("time = %fms\n", elapsed_ms);
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    printf("[task] power off\n");

    return 0;
}
