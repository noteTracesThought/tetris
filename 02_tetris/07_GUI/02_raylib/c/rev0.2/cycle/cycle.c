#include "../cycle/cycle.h"
#include "../cycle/cycle_config.h"
#include "../cycle/cycle_process.h"
#include "../input/input.h"
#include <stdint.h>
#include <time.h>

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/
#define     ONE_MS_IN_NS        1000000LL       /* 1ミリ秒 = 1,000,000 ナノ秒 */
#define     ONE_SECOND_IN_NS    1000000000LL    /* 1秒 = 1,000,000,000 ナノ秒 */
#define     MS                  1000U           /* 1ms */
#define     CYCLE_CURRENT_MS    (MS + 1U)       /* cal 1ms count */

/*----------------------------*/
/* variable */
/*----------------------------*/
static int process_items;
static struct timespec current_time_start;
static int current_ms;
static int process_elapsed[ID_MAX];    /* インターバル管理 */
static int cyclecnt;

/*----------------------------*/
/* function section */
/*----------------------------*/
int cycle_add_ms(void);

/*----------------------------*/
/* public function */
/*----------------------------*/
void cycle_init(void)
{
    // current_time_start = clock();
    clock_gettime(CLOCK_MONOTONIC, &current_time_start);
    current_ms = 0;
    cyclecnt = 0;
    for(int cnt = 0; cnt < ID_MAX; cnt++)
    {
        process_elapsed[cnt] = 0;
    }
    cycle_process_init();
}

void cycle_mainloop(void)
{
    int passed_ms;

    /* キー入力は毎ループ（1ms未満の極小間隔）でチェックして取りこぼしを防ぐ */
    passed_ms = cycle_add_ms();
    if(passed_ms > 0)
    {
        for(int cnt = 0; cnt < ID_MAX; cnt++)
        {
            process_elapsed[cnt] += passed_ms;
            /* 毎周期処理させるべきではない。首が回らないので外出しし、マルチプロセスに耐えうる状態に備える。 */
        }
    }
}

void cycle_process_run(void)
{
    int cnt = cyclecnt;                 /* 将来割り込み処理を入れたときに備えてラッチする */
    int cyc = cycle_index[cnt].cycle;   /* .cycle で整数の周期を取得 */
    if(process_elapsed[cnt] >= cyc)
    {
        process_elapsed[cnt] -= cyc;
        /* None(NULL)対策を含めた関数ポインタの実行 */
        if(cycle_index[cnt].func != NULL)
        {
            // printf("cycle_process_run: cnt = %d, cyc = %d, process_elapsed[cnt] = %ld\n", cnt, cyc, process_elapsed[cnt]);
            cycle_index[cnt].func();    /* None対策必要 */
        }
    }

    if(cnt >= ID_MAX - 1)
    {
        cnt = 0;
    }
    else
    {
        cnt++;
    }
    cyclecnt = cnt;
}

/*----------------------------*/
/* private function */
/*----------------------------*/
int cycle_add_ms(void)
{
    struct timespec now;
    long long elapsed_ns;
    int passed_ms;

    if (clock_gettime(CLOCK_MONOTONIC, &now) != 0)
    {
        return 0;
    }

    elapsed_ns =
        (long long)(now.tv_sec - current_time_start.tv_sec)
            * ONE_SECOND_IN_NS
        + (now.tv_nsec - current_time_start.tv_nsec);

    if (elapsed_ns < ONE_MS_IN_NS)
    {
        return 0;
    }

    passed_ms = (int)(elapsed_ns / ONE_MS_IN_NS);
    current_ms = (current_ms + passed_ms) % CYCLE_CURRENT_MS;

    /* 経過した整数ミリ秒分だけ基準時刻を進め、端数を保持する */
    current_time_start.tv_nsec += passed_ms * ONE_MS_IN_NS;

    /* tv_nsec が秒の範囲を超えた分を tv_sec に繰り上げる */
    current_time_start.tv_sec += current_time_start.tv_nsec / ONE_SECOND_IN_NS;
    current_time_start.tv_nsec %= ONE_SECOND_IN_NS;

    return passed_ms;
}
