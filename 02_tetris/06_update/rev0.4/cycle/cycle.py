import time
from board.board import Board
from block.block import Blocks
from settings import OS_ENVIROMENT, \
                     LINUX, \
                     WINDOWS

from input.input import Input
from game.position import MovePosition

if OS_ENVIROMENT == LINUX:
    import sys
    import termios
    import tty
elif OS_ENVIROMENT == WINDOWS:
    import msvcrt
else:
    # Do Nothing
    pass
TARGET_INTERVAL_NS = 1_000_000  # 1ms = 1,000,000ナノ秒
  
class Cycle:
    def __init__(self, blocks:Blocks, board:Board, input:Input, pos:MovePosition):
        self.blocks = blocks
        self.board = board
        self.input = input
        self.pos   = pos

        # ループ開始
        self.next_time = time.perf_counter_ns() + TARGET_INTERVAL_NS
        self.current_ms = 0
        self.PROCESS_ITEMS = {
            # "1": self.cycle_process_1ms,
            # "2": self.cycle_process_2ms,
            # "4": self.cycle_process_4ms,
            # "10": self.cycle_process_10ms,
            "50": self.cycle_process_50ms,
            "100": self.cycle_process_100ms,
            "500": self.cycle_process_500ms,
            "1000": self.cycle_process_1000ms,
        }

    def cycle_mainloop(self):
        self.cycle_add_ms()
        for key, value in self.PROCESS_ITEMS.items():
            cycle = self.current_ms % int(key)
            # print(f"self.current_ms:{self.current_ms}, cycle:{cycle}")
            if (self.current_ms > 0) and (cycle <= 0):
                self.PROCESS_ITEMS[key]()

    def cycle_add_ms(self):
        # 待機処理（ビジーループ方式で精度を向上）
        while time.perf_counter_ns() < self.next_time:
            pass  # 目標時刻になるまでひたすら待つ
        self.next_time = time.perf_counter_ns() + TARGET_INTERVAL_NS
        if self.current_ms >= 1000:
            self.current_ms = 0          # 1s経過
        else:
            self.current_ms += 1         # 1〜999msまで加算

    def cycle_process_1ms(self):
        # print("[proc] process_1ms")
        pass

    def cycle_process_2ms(self):
        # print("[proc] process_2ms")
        pass

    def cycle_process_4ms(self):
        # print("[proc] process_4ms")
        pass

    def cycle_process_10ms(self):
        # print("[proc] process_10ms")
        pass

    def cycle_process_50ms(self):
        # print("[proc] process_50ms")
        pass

    def cycle_process_100ms(self):
        # print("[proc] process_100ms")
        pass

    def cycle_process_500ms(self):
        # print("[proc] process_500ms")
        block = self.blocks.import_block()
        self.board.update_view(block)
        self.input.input_putkey()

    def cycle_process_1000ms(self):
        # print("[proc] process_1000ms")
        self.pos.current.y += 1
        # pass
