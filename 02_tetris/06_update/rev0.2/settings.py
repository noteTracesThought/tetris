
WINDOWS           = "Windows"
LINUX             = "Linux"

# -----------------------------------------------
# settings
# -----------------------------------------------
# OS : Windows or Linux
OS_ENVIROMENT      = LINUX      # selection WINDOWS or LINUX

# keyboard
KEY_HARD_DROP      = 'h'        # 一気に下へ落とす
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
SCORE_MULTIPLIER = (0, 1, 1.2, 1.5, 2)
