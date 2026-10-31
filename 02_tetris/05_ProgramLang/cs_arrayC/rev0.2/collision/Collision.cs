namespace Tetris
{
    /// <summary>
    /// update check header
    /// update check functions
    ///
    /// Todo:
    ///     * rotate
    /// </summary>
    public static class Collision
    {
        public static bool is_invalid_position(int[,,] block, int x, int y, int rotation)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[check] is_invalid_position");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            bool is_invalid = false;
            bool is_invalid_move = is_out_of_board(block, x, y, rotation);
            bool is_invalid_rotate = Block.check_operation_rotate();
            if (is_invalid_move || is_invalid_rotate)
            {
                is_invalid = true;
            }
            return is_invalid;
        }

        public static bool is_out_of_board(int[,,] block, int x, int y, int rotation)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[check] is_out_of_board");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            bool is_invalid = false;
            int block_width = Block.get_block_width(block, rotation);
            int block_height = Block.get_block_height(block, rotation);
            if (x < 0)
            {
                is_invalid = true;
            }
            if (y < 0)
            {
                is_invalid = true;
            }
            if (x > Settings.BOARD_SIZE_WIDTH - block_width)
            {
                is_invalid = true;
            }
            if (y > Settings.BOARD_SIZE_HEIGHT - block_height)
            {
                is_invalid = true;
            }
            return is_invalid;
        }

        public static bool check_collision_detection(int[,,] block, int next_x, int next_y, int rotation)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[check] check_collision_detection");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            int block_height = Block.get_block_height(block, rotation);

            for (int r = 0; r < 4; r++)
            {
                for (int c = 0; c < 4; c++)
                {
                    // 衝突検知(床)
                    if (next_y >= Settings.BOARD_SIZE_HEIGHT - block_height)
                    {
                        // Console.WriteLine($"next_y:{next_y}");
                        return true;
                    }

                    // next(blockなし)
                    if (block[rotation, r, c] != 1)
                    {
                        continue;
                    }

                    // 衝突検知(board block)
                    if (Settings.board_result[next_y + r, next_x + c] == 1)
                    {
                        // Console.WriteLine($"next_y+r:{next_y + r}");
                        // Console.WriteLine($"next_x+c:{next_x + c}");
                        return true;
                    }

                    // 衝突検知(next board block)
                    if (Settings.board_result[next_y + r + 1, next_x + c] == 1)
                    {
                        // Console.WriteLine($"next_y+r+1:{next_y + r + 1}");
                        // Console.WriteLine($"next_x+c:{next_x + c}");
                        return true;
                    }
                }
            }

            return false;
        }

        // ▼▼▼ ハードドロップ機能追加 ▼▼▼
        public static int execute_hard_drop(int[,,] block, int x, int y, int rotation)
        {
            // ハードドロップを実行する
            int current_y = y;
            int next_y = y;

            while (true)
            {
                // 仮想的に1段下の位置（Position）を計算して next にセットするだけ
                // (Python版のtry/exceptは実質到達しないため、単純なループとして実装)
                next_y += 1;

                // その1段下（next）で衝突するかチェック
                if (check_collision_detection(block, x, next_y, rotation))
                {
                    // ぶつかるなら、今の current（衝突する直前の安全な位置）が最終位置なので終了
                    break;
                }

                // ぶつからなければ、現在位置(current)を1段下に進めて次のループへ
                current_y = next_y;
            }
            next_y = current_y;

            return next_y;
        }
        // ▲▲▲ ハードドロップ機能追加 ▲▲▲
    }
}
