namespace Tetris
{
    /// <summary>
    /// -----------------------------------------------
    /// settings
    /// -----------------------------------------------
    /// tetris main task header
    /// tetris main task functions
    ///
    /// Todo:
    ///     * 側面衝突検知時は壁扱いとなるように修正すること
    ///     * ブロックが側面の壁に到達しない
    ///     * 周期タスク処理
    /// </summary>
    public static class Settings
    {
        public const string WINDOWS = "Windows";
        public const string LINUX = "Linux";

        // OS : Windows or Linux
        public static string OS_ENVIROMENT = LINUX;   // selection WINDOWS or LINUX

        // keyboard
        // ▼▼▼ ハードドロップ機能追加 ▼▼▼
        public const char KEY_HARD_DROP = 'h';        // 一気に下へ落とす
        // ▲▲▲ ハードドロップ機能追加 ▲▲▲
        public const char KEY_DROP = ' ';              // 下へ加速
        public const char KEY_LEFT = 's';               // 左へ移動
        public const char KEY_RIGHT = 'd';              // 右へ移動
        public const char KEY_ROTATION_RIGHT = 'r';     // ブロックを右回転
        public const char KEY_ROTATION_LEFT = 'w';      // ブロックを左回転
        public const char KEY_GAME_FINISH = 'q';        // ゲームを強制終了させる
        // -----------------------------------------------

        // const
        public const int BOARD_SIZE_HEIGHT = 20;   // board height
        public const int BOARD_SIZE_WIDTH = 10;    // board width

        // ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
        public static readonly double[] SCORE_MULTIPLIER = { 0, 1, 1.2, 1.5, 2 };
        // ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲

        // global
        public static int[,] board_result = new int[BOARD_SIZE_HEIGHT, BOARD_SIZE_WIDTH]; // 永続状態
        public static int[,] board = new int[BOARD_SIZE_HEIGHT, BOARD_SIZE_WIDTH];         // 描画用
    }
}
