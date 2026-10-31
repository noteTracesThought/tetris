import time

from input.input import input_putkey
from cycle.cycle_config import (
    CYCLE_ID, 
    cycle_index
)

global PROCESS_ITEMS
ONE_MS_IN_NS  = 1_000_000    # 1ミリ秒 = 1,000,000 ナノ秒
FALL_SPEED_MS = 1_000        # ブロックが落ちる周期（1000msごと）
MS            = 1000         # 1ms
CYCLE_CURRENT_MS = MS + 1    # cal 1ms count
CPU_SLEEP     = 0.01         # 10ms

current_time_start = 0
current_ms = 0
process_elapsed = {}

def cycle_init():
    global current_time_start
    global current_ms
    global process_elapsed
    global PROCESS_ITEMS

    current_time_start = time.perf_counter_ns()
    current_ms = 0

    PROCESS_ITEMS = {
        interval: func
        for _, interval, func in cycle_index
        if func is not None
    }

    process_elapsed = {
        interval: 0
        for interval in PROCESS_ITEMS
    }

def cycle_mainloop():
    # キー入力は毎ループ（1ms未満の極小間隔）でチェックして取りこぼしを防ぐ
    passed_ms = cycle_add_ms()

    if passed_ms > 0:
        for interval, func in PROCESS_ITEMS.items():
            process_elapsed[interval] += passed_ms

            if process_elapsed[interval] >= interval:
                process_elapsed[interval] -= interval
                func()
    # time.sleep(CPU_SLEEP) sleep control is call function

def cycle_add_ms():
    global current_time_start
    global current_ms

    now = time.perf_counter_ns()
    t = now - current_time_start
    if t >= ONE_MS_IN_NS:                   # 1ms経過
        # 実際に経過したミリ秒数を計算（処理の遅延で1ms以上経っていた場合も吸収）
        passed_ms = t // ONE_MS_IN_NS       # 切り捨て
        current_ms = (current_ms + passed_ms) % CYCLE_CURRENT_MS  # 0〜1000msで循環
        
        # 加算したミリ秒分だけ開始時間を進める（時間のズレ・積算誤差を防止）
        current_time_start += passed_ms * ONE_MS_IN_NS
    #     return True  # 1ms更新された
    # return False  # まだ1ms経っていない
        return passed_ms
    return 0
