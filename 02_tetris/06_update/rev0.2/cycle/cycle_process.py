from cycle.cycle_types import CYCLE_ID

need_render_fall = need_render_fall = [False] * CYCLE_ID.ID_MAX

def pop_fall_event():
    """落下・再描画フラグを取得し、リセットする"""

    index = CYCLE_ID.ID_1000
    if need_render_fall[index]:
        need_render_fall[index] = False
        return True
    return False

def set_need_fall(index):
    """落下・再描画フラグを有効にする"""
    need_render_fall[index] = True

def cycle_process_1ms():
    # print("[proc] process_1ms")
    pass

def cycle_process_2ms():
    # print("[proc] process_2ms")
    pass

def cycle_process_4ms():
    # print("[proc] process_4ms")
    pass

def cycle_process_10ms():
    # print("[proc] process_10ms")
    pass

def cycle_process_50ms():
    # print("[proc] process_50ms")
    pass

def cycle_process_100ms():
    # print("[proc] process_100ms")
    pass

def cycle_process_500ms():
    # print("[proc] process_500ms")
    pass

def cycle_process_1000ms():
    # print("[proc] process_1000ms")
    set_need_fall(CYCLE_ID.ID_1000)
    pass
