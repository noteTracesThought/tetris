using System;
using System.Collections.Generic;
using System.Text;

namespace Tetris
{
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
            Settings.board = (int[,])Settings.board_result.Clone();
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
            var newBoard = new List<int[]>();

            for (int r = 0; r < Settings.BOARD_SIZE_HEIGHT; r++)
            {
                int ones = 0;
                var row = new int[Settings.BOARD_SIZE_WIDTH];
                for (int c = 0; c < Settings.BOARD_SIZE_WIDTH; c++)
                {
                    row[c] = Settings.board_result[r, c];
                    if (row[c] == 1)
                    {
                        ones++;
                    }
                }
                if (ones < Settings.BOARD_SIZE_WIDTH)
                {
                    newBoard.Add(row);
                }
            }

            while (newBoard.Count < Settings.BOARD_SIZE_HEIGHT)
            {
                // new_board.insert(0, [0]*BOARD_SIZE_WIDTH) 相当
                newBoard.Insert(0, new int[Settings.BOARD_SIZE_WIDTH]);
            }

            var result = new int[Settings.BOARD_SIZE_HEIGHT, Settings.BOARD_SIZE_WIDTH];
            for (int r = 0; r < Settings.BOARD_SIZE_HEIGHT; r++)
            {
                for (int c = 0; c < Settings.BOARD_SIZE_WIDTH; c++)
                {
                    result[r, c] = newBoard[r][c];
                }
            }
            Settings.board_result = result;
        }

        public static List<int> get_bingo_lines()
        {
            var delete_rows = new List<int>();

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
                        delete_rows.Add(r);
                        Console.WriteLine("bingo!!");
                    }
                }
            }
            return delete_rows;
        }
    }
}
