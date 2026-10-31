#include "Settings.hpp"

namespace settings {

/* OS : Windows or Linux */
std::string OS_ENVIROMENT = LINUX;      /* selection WINDOWS or LINUX */

/* ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼ */
const std::array<double, 5> SCORE_MULTIPLIER = {0, 1, 1.2, 1.5, 2};
/* ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲ */

/* global */
BoardArray board_result{};   /* 永続状態 */
BoardArray board{};          /* 描画用 */

} // namespace settings
