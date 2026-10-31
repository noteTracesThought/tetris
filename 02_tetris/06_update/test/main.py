import os
import sys
import time
import select
import tty
import termios

def main():
    # ターミナルの設定を「Enterなしで即時入力＆画面に文字を表示しない」モードにする（Mac/Linux用）
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd) # これで1文字押した瞬間にPythonに通知される

        # 周期管理用のカウンター（ミリ秒）
        drop_timer = 0
        FALL_INTERVAL = 500  # 500ms周期で自動落下

        last_time = time.perf_counter_ns()
        
        # 標準出力のバッファリングを無効化して即時描画
        sys.stdout.write("ゲーム開始! [A]:左 [D]:右 [W]:回転 [S]:高速落下 [Q]:終了\r\n")
        sys.stdout.flush()
        
        while True:
            now = time.perf_counter_ns()
            dt = (now - last_time) / 1_000_000  # 経過時間をミリ秒に変換
            last_time = now

            drop_timer += dt

            # 1. 【500ms周期】ミノの自動落下処理
            if drop_timer >= FALL_INTERVAL:
                sys.stdout.write("--- ミノが1マス自動落下 ---\r\n")
                sys.stdout.flush()
                drop_timer = 0

            # 2. 【超高感度】キー入力を10ms待機しつつ監視（スリープの代わり）
            # 10msの間、キーが押されるのを待ちます。押されなければタイムアウトして次に進みます。
            rlist, _, _ = select.select([sys.stdin], [], [], 0.010)
            
            if rlist:
                # キーボードが押されたら、ここが1ms未満で即座に実行されます！
                key = sys.stdin.read(1)
                
                if key in ('q', 'Q'):
                    sys.stdout.write("\r\nゲームを終了します。\r\n")
                    sys.stdout.flush()
                    break
                elif key in ('a', 'A'):
                    sys.stdout.write("左に移動\r\n")
                elif key in ('d', 'D'):
                    sys.stdout.write("右に移動\r\n")
                elif key in ('w', 'W'):
                    sys.stdout.write("ミノを回転\r\n")
                elif key in ('s', 'S'):
                    sys.stdout.write("下へ加速\r\n")
                
                sys.stdout.flush()

    finally:
        # プログラム終了時、またはエラー時に必ずターミナルの設定を元に戻す
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    main()