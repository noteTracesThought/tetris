using System;
using System.Text;

namespace Tetris
{
    /// <summary>
    /// get_bingo_lines() の戻り値 (Pythonのlistに相当、通常の固定長配列で実装)
    /// </summary>
    public struct bingo_lines_t
    {
        public int[] rows;
        public int count;
    }

    public static class Board
    {
        public static void update_view(int[,,] block, int x, int y, int rotation)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[view] update_view");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲

            // view
            load_board_result();                   // おばけ(残像)を消す
            for (int r = 0; r < 4; r++)
            {
                for (int c = 0; c < 4; c++)
                {
                    if (block[rotation, r, c] == 1)
                    {
                        Settings.board[y + r, x + c] = 1;
                        // Console.WriteLine($"r+y: {r + y}");
                        // Console.WriteLine($"c+x: {c + x}");
                    }
                }
            }
            draw_board(Settings.board);
        }

        /// <summary>
        /// board header
        /// group board functions
        /// </summary>
        public static void init_board()
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[init] init_board");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            create_board();
        }

        public static void create_board()
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[init] create_board");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            Settings.board_result = new int[Settings.BOARD_SIZE_HEIGHT, Settings.BOARD_SIZE_WIDTH];
            Settings.board = new int[Settings.BOARD_SIZE_HEIGHT, Settings.BOARD_SIZE_WIDTH];
        }

        public static void load_board_result()
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[init] load_board_result");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            for (int r = 0; r < Settings.BOARD_SIZE_HEIGHT; r++)
            {
                for (int c = 0; c < Settings.BOARD_SIZE_WIDTH; c++)
                {
                    Settings.board[r, c] = Settings.board_result[r, c];
                }
            }
        }

        public static void draw_board(int[,] board)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[proc] draw_board");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            for (int r = 0; r < board.GetLength(0); r++)
            {
                var line = new StringBuilder();
                for (int c = 0; c < board.GetLength(1); c++)
                {
                    line.Append(board[r, c] == 0 ? '\u25A1' : '\u25A0'); // □ / ■
                }
                Console.WriteLine(line.ToString());
            }
        }

        public static void clear_bingo_lines()
        {
            int[,] new_board = new int[Settings.BOARD_SIZE_HEIGHT, Settings.BOARD_SIZE_WIDTH];
            int new_board_count = 0;

            for (int r = 0; r < Settings.BOARD_SIZE_HEIGHT; r++)
            {
                int ones = 0;
                for (int c = 0; c < Settings.BOARD_SIZE_WIDTH; c++)
                {
                    if (Settings.board_result[r, c] == 1)
                    {
                        ones++;
                    }
                }
                if (ones < Settings.BOARD_SIZE_WIDTH)
                {
                    for (int c = 0; c < Settings.BOARD_SIZE_WIDTH; c++)
                    {
                        new_board[new_board_count, c] = Settings.board_result[r, c];
                    }
                    new_board_count++;
                }
            }

            while (new_board_count < Settings.BOARD_SIZE_HEIGHT)
            {
                // new_board.insert(0, [0]*BOARD_SIZE_WIDTH) 相当
                for (int r = new_board_count; r > 0; r--)
                {
                    for (int c = 0; c < Settings.BOARD_SIZE_WIDTH; c++)
                    {
                        new_board[r, c] = new_board[r - 1, c];
                    }
                }
                for (int c = 0; c < Settings.BOARD_SIZE_WIDTH; c++)
                {
                    new_board[0, c] = 0;
                }
                new_board_count++;
            }

            Settings.board_result = new_board;
        }

        public static bingo_lines_t get_bingo_lines()
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
    }
}
