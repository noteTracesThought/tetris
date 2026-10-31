#ifndef SETTINGS_H
#define SETTINGS_H

/* -----------------------------------------------
 * settings
 * ----------------------------------------------- */
/* OS : Windows or Linux */
#define WINDOWS "Windows"
#define LINUX   "Linux"

extern const char *OS_ENVIROMENT;   /* selection WINDOWS or LINUX */

/* keyboard */
/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
#define KEY_HARD_DROP      'h'   /* 一気に下へ落とす */
/* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
#define KEY_DROP           ' '   /* 下へ加速 */
#define KEY_LEFT           's'   /* 左へ移動 */
#define KEY_RIGHT          'd'   /* 右へ移動 */
#define KEY_ROTATION_RIGHT 'r'   /* ブロックを右回転 */
#define KEY_ROTATION_LEFT  'w'   /* ブロックを左回転 */
#define KEY_GAME_FINISH    'q'   /* ゲームを強制終了させる */
/* ----------------------------------------------- */

/* tetris main task header
 * tetris main task functions
 *
 * Todo:
 *     * 側面衝突検知時は壁扱いとなるように修正すること
 *     * ブロックが側面の壁に到達しない
 *     * 周期タスク処理
 */

/* const */
#define BOARD_SIZE_HEIGHT 20   /* board height */
#define BOARD_SIZE_WIDTH  10   /* board width */

/* ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼ */
extern const double SCORE_MULTIPLIER[5];
/* ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲ */

/* global */
extern int board_result[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH]; /* 永続状態 */
extern int board[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH];        /* 描画用 */

#endif /* SETTINGS_H */
