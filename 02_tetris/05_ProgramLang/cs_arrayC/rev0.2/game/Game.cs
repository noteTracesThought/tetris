using System;

namespace Tetris
{
    /// <summary>
    /// tetris main task header
    /// tetris main task functions
    ///
    /// Todo:
    ///     * 側面衝突検知時は壁扱いとなるように修正すること
    ///     * ブロックが側面の壁に到達しない
    ///     * 周期タスク処理
    /// </summary>
    public static class Game
    {
        public static void power_on_game()
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[task] power on");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            init_game();

            char put_key = '\0';
            int[,,] block = Block.get_block();
            int x = 3;
            int y = 0;
            double score = 0;
            int rotation = 0;
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            int proc_cnt = 0;
            char[] commands = {
                Settings.KEY_DROP,
                Settings.KEY_LEFT,
                Settings.KEY_RIGHT,
                Settings.KEY_ROTATION_LEFT,
                Settings.KEY_ROTATION_RIGHT,
                Settings.KEY_HARD_DROP,
            };
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            while (put_key != Settings.KEY_GAME_FINISH)
            {
                // ▼▼▼ 処理速度計測（10万回） ▼▼▼
                if (false)
                {
                    if (Settings.OS_ENVIROMENT == Settings.LINUX)
                    {
                        put_key = Input.getch_for_Linux();
                    }
                    else if (Settings.OS_ENVIROMENT == Settings.WINDOWS)
                    {
                        if (Console.KeyAvailable)
                        {
                            put_key = Console.ReadKey(true).KeyChar;
                        }
                    }
                    else
                    {
                        put_key = (char)Console.Read();
                    }
                }
                else
                {
                    if (proc_cnt < 1_000_000)
                    {
                        put_key = commands[proc_cnt % 6];
                        proc_cnt += 1;
                    }
                    else
                    {
                        break;              // 10万回計測完了
                    }
                }
                // ▲▲▲ 処理速度計測（10万回） ▲▲▲

                rotation = Input.request_operation_rotate(put_key, block, x, y, rotation);
                // ▼▼▼ ハードドロップ機能追加 ▼▼▼
                (int next_x, int next_y) = Input.get_next_position(put_key, block, x, y, rotation);
                // ▲▲▲ ハードドロップ機能追加 ▲▲▲
                if (Collision.is_invalid_position(block, next_x, next_y, rotation))
                {
                    next_x = x;
                    next_y = y;
                }

                // 衝突検知
                if (Collision.check_collision_detection(block, next_x, next_y, rotation))
                {
                    Block.fix_block(block, next_x, next_y, rotation);  // update board result
                    // Console.WriteLine($"x={x}");
                    // Console.WriteLine($"y={y}");
                    // Console.WriteLine($"next_x={next_x}");
                    // Console.WriteLine($"next_y={next_y}");

                    // ▼▼▼ 処理速度計測（10万回） ▼▼▼
                    // // game over
                    // if (is_game_over(put_key) == true) {
                    //     Console.WriteLine("game over!");
                    //     break;
                    // }
                    // ▲▲▲ 処理速度計測（10万回） ▲▲▲

                    // bingo
                    bingo_lines_t bingo_lines = get_bingo_lines();
                    // ▼▼▼ 処理速度が影響していた処理を追加 ▼▼▼
                    if (bingo_lines.count > 0)
                    {
                        // ▲▲▲ 処理速度が影響していた処理を追加 ▲▲▲
                        // ▼▼▼ 設計変更対応（スコア倍率変更） ▼▼▼
                        // score += bingo_lines.count;
                        score += bingo_lines.count * Settings.SCORE_MULTIPLIER[bingo_lines.count];
                        // ▲▲▲ 設計変更対応（スコア倍率変更） ▲▲▲
                        Board.clear_bingo_lines();
                    }

                    block = Block.get_block();
                    // Console.WriteLine(block);
                    x = 3;
                    y = 0;
                    rotation = 0;
                }
                else
                {
                    x = next_x;
                    y = next_y;
                }

                // Console.WriteLine(rotation);
                // ▼▼▼ 処理速度計測（10万回） ▼▼▼
                // Board.update_view(block, x, y, rotation);
            }
            // Console.WriteLine($"score : {score * 100}");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
        }

        /// <summary>
        /// initialize header
        /// initialize functions
        /// </summary>
        public static void init_game()
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[init] initialize");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            Board.init_board();
            Block.create_blocks();
        }

        // game.py では board.board から get_bingo_lines を import した後、
        // モジュール末尾で同名の get_bingo_lines() を再定義しているため、
        // power_on_game() 内ではこのローカル版(Board側とロジックは同一)が使用される。
        // C#では static class 単位で名前空間が分かれるため、Game.get_bingo_lines() として
        // Board.get_bingo_lines() とは別に同名メソッドを定義することでこの「上書き」を再現する。
        private static bingo_lines_t get_bingo_lines()
        {
            bingo_lines_t delete_rows;
            delete_rows.rows = new int[Settings.BOARD_SIZE_HEIGHT];
            delete_rows.count = 0;

            for (int r = 0; r < Settings.BOARD_SIZE_HEIGHT; r++)
            {
                for (int c = 0; c < Settings.BOARD_SIZE_WIDTH; c++)
                {
                    if (Settings.board_result[r, c] != 1)
                    {
                        break;
                    }
                    if (c >= Settings.BOARD_SIZE_WIDTH - 1)
                    {
                        delete_rows.rows[delete_rows.count++] = r;
                        Console.WriteLine("bingo!!");
                    }
                }
            }
            return delete_rows;
        }

        public static bool is_game_over(char put_key)
        {
            int next_y;
            if (put_key == Settings.KEY_DROP)
            {
                next_y = 1;
            }
            else
            {
                next_y = 0;
            }
            for (int c = 0; c < Settings.BOARD_SIZE_WIDTH; c++)
            {
                if (Settings.board_result[next_y, c] == 1)
                {
                    return true;
                }
            }
            return false;
        }
    }
}
