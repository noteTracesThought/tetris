#ifndef SETTINGS_HPP
#define SETTINGS_HPP

namespace settings {

/* -----------------------------------------------
 * settings
 * ----------------------------------------------- */
/* OS : Windows or Linux */
extern const char *WINDOWS;
extern const char *LINUX;

extern const char *OS_ENVIROMENT;   /* selection WINDOWS or LINUX */

/* keyboard */
/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
const char KEY_HARD_DROP      = 'h';   /* 一気に下へ落とす */
/* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
const char KEY_DROP           = ' ';   /* 下へ加速 */
const char KEY_LEFT           = 's';   /* 左へ移動 */
const char KEY_RIGHT          = 'd';   /* 右へ移動 */
const char KEY_ROTATION_RIGHT = 'r';   /* ブロックを右回転 */
const char KEY_ROTATION_LEFT  = 'w';   /* ブロックを左回転 */
const char KEY_GAME_FINISH    = 'q';   /* ゲームを強制終了させる */
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
const int BOARD_SIZE_HEIGHT = 20;   /* board height */
const int BOARD_SIZE_WIDTH  = 10;   /* board width */

/* ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼ */
extern const double SCORE_MULTIPLIER[5];
/* ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲ */

/* global (std::vector / std::array を使わない通常の固定長配列) */
extern int board_result[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH]; /* 永続状態 */
extern int board[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH];        /* 描画用 */

} // namespace settings

#endif // SETTINGS_HPP
