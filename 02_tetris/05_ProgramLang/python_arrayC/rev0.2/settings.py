import array

WINDOWS           = "Windows"
LINUX             = "Linux"

# -----------------------------------------------
# settings
# -----------------------------------------------
# OS : Windows or Linux
OS_ENVIROMENT      = LINUX      # selection WINDOWS or LINUX

# keyboard
# ▼▼▼ ハードドロップ機能追加 ▼▼▼
KEY_HARD_DROP      = 'h'        # 一気に下へ落とす
# ▲▲▲ ハードドロップ機能追加 ▲▲▲
KEY_DROP           = ' '        # 下へ加速
KEY_LEFT           = 's'        # 左へ移動
KEY_RIGHT          = 'd'        # 右へ移動
KEY_ROTATION_RIGHT = 'r'        # ブロックを右回転
KEY_ROTATION_LEFT  = 'w'        # ブロックを左回転
KEY_GAME_FINISH    = 'q'        # ゲームを強制終了させる
# -----------------------------------------------

'''tetris main task header
tetris main task functions

Todo:
    * 側面衝突検知時は壁扱いとなるように修正すること
    * ブロックが側面の壁に到達しない
    * 周期タスク処理
'''

# const
BOARD_SIZE_HEIGHT = 20      # board height
BOARD_SIZE_WIDTH  = 10      # board width
# ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
# ▼▼▼ list を使用せず、型指定した固定長配列(array.array)で実装 ▼▼▼
SCORE_MULTIPLIER = array.array('d', (0, 1, 1.2, 1.5, 2))
# ▲▲▲ list を使用せず、型指定した固定長配列(array.array)で実装 ▲▲▲
# ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲

# global
# ▼▼▼ list を使用せず、型指定した固定長配列(array.array)で実装 ▼▼▼
board_result = None         # 永続状態 (int型 array.array を行として持つ tuple : C言語の int[H][W] 相当)
board = None                # 描画用   (int型 array.array を行として持つ tuple : C言語の int[H][W] 相当)
# ▲▲▲ list を使用せず、型指定した固定長配列(array.array)で実装 ▲▲▲
block_map_key = None        # block map key (str : 1文字キーの並び)
block_map = None            # blocks
