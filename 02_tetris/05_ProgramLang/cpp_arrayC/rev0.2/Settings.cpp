#include "Settings.hpp"

namespace settings {

/* OS : Windows or Linux */
const char *WINDOWS = "Windows";
const char *LINUX   = "Linux";

const char *OS_ENVIROMENT = LINUX;      /* selection WINDOWS or LINUX */

/* ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼ */
const double SCORE_MULTIPLIER[5] = {0, 1, 1.2, 1.5, 2};
/* ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲ */

/* global */
int board_result[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH]; /* 永続状態 */
int board[BOARD_SIZE_HEIGHT][BOARD_SIZE_WIDTH];        /* 描画用 */

} // namespace settings
