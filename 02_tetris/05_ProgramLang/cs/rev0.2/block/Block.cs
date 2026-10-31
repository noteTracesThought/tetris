using System;
using System.Collections.Generic;

namespace Tetris
{
    public static class Block
    {
        // 各ブロックは [rotation(TOP,RIGHT,BOTTOM,LEFT), row, col] の順で定義
        private static readonly int[,,] I = {
            {{1,1,1,1},{0,0,0,0},{0,0,0,0},{0,0,0,0}},
            {{0,0,0,1},{0,0,0,1},{0,0,0,1},{0,0,0,1}},
            {{0,0,0,0},{0,0,0,0},{0,0,0,0},{1,1,1,1}},
            {{1,0,0,0},{1,0,0,0},{1,0,0,0},{1,0,0,0}}
        };

        private static readonly int[,,] J = {
            {{0,1,1,1},{0,0,0,1},{0,0,0,0},{0,0,0,0}},
            {{0,0,0,0},{0,0,0,1},{0,0,0,1},{0,0,1,1}},
            {{0,0,0,0},{0,0,0,0},{1,0,0,0},{1,1,1,0}},
            {{1,1,0,0},{1,0,0,0},{1,0,0,0},{0,0,0,0}}
        };

        private static readonly int[,,] L = {
            {{1,1,1,0},{1,0,0,0},{0,0,0,0},{0,0,0,0}},
            {{0,0,1,1},{0,0,0,1},{0,0,0,1},{0,0,0,0}},
            {{0,0,0,0},{0,0,0,0},{0,0,0,1},{0,1,1,1}},
            {{0,0,0,0},{1,0,0,0},{1,0,0,0},{1,1,0,0}}
        };

        private static readonly int[,,] S = {
            {{0,0,1,1},{0,1,1,0},{0,0,0,0},{0,0,0,0}},
            {{0,0,0,0},{0,0,1,0},{0,0,1,1},{0,0,0,1}},
            {{0,0,0,0},{0,0,0,0},{0,1,1,0},{1,1,0,0}},
            {{1,0,0,0},{1,1,0,0},{0,1,0,0},{0,0,0,0}}
        };

        private static readonly int[,,] Z = {
            {{0,1,1,0},{0,0,1,1},{0,0,0,0},{0,0,0,0}},
            {{0,0,0,0},{0,0,0,1},{0,0,1,1},{0,0,1,0}},
            {{0,0,0,0},{0,0,0,0},{1,1,0,0},{0,1,1,0}},
            {{0,1,0,0},{1,1,0,0},{1,0,0,0},{0,0,0,0}}
        };

        private static readonly int[,,] O = {
            {{0,0,1,1},{0,0,1,1},{0,0,0,0},{0,0,0,0}},
            {{0,0,0,0},{0,0,0,0},{0,0,1,1},{0,0,1,1}},
            {{0,0,0,0},{0,0,0,0},{1,1,0,0},{1,1,0,0}},
            {{1,1,0,0},{1,1,0,0},{0,0,0,0},{0,0,0,0}}
        };

        private static readonly int[,,] T = {
            {{0,0,1,0},{0,1,1,1},{0,0,0,0},{0,0,0,0}},
            {{0,0,0,0},{0,0,1,0},{0,0,1,1},{0,0,1,0}},
            {{0,0,0,0},{0,0,0,0},{1,1,1,0},{0,1,0,0}},
            {{0,1,0,0},{1,1,0,0},{0,1,0,0},{0,0,0,0}}
        };

        // global (settings.py の block_map_key / block_map に相当)
        public static List<char> block_map_key = new List<char>();
        public static Dictionary<char, int[,,]> block_map = new Dictionary<char, int[,,]>();

        // ▼▼▼ 処理速度計測（10万回） ▼▼▼
        private static readonly Random random = new Random(1234567);
        // ▲▲▲ 処理速度計測（10万回） ▲▲▲

        public static void create_blocks()
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[init] create_blocks");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            block_map_key = new List<char>();
            block_map = new Dictionary<char, int[,,]>
            {
                { 'I', I },
                { 'J', J },
                { 'L', L },
                { 'S', S },
                { 'Z', Z },
                { 'O', O },
                { 'T', T },
            };
            foreach (char key in block_map.Keys)
            {
                block_map_key.Add(key);
            }
        }

        public static int[,,] get_block()
        {
            char selected = block_map_key[random.Next(block_map_key.Count)];
            return block_map[selected];
        }

        public static int get_block_width(int[,,] block, int rotation)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[check] get_block_width");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            int width = 0;
            for (int row = 0; row < 4; row++)
            {
                for (int col = 0; col < 4; col++)
                {
                    if (block[rotation, row, col] == 1)
                    {
                        width = Math.Max(width, col + 1);
                    }
                }
            }
            return width;
        }

        public static int get_block_height(int[,,] block, int rotation)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[check] get_block_height");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            int height = 0;
            for (int row = 0; row < 4; row++)
            {
                bool hasBlock = false;
                for (int col = 0; col < 4; col++)
                {
                    if (block[rotation, row, col] == 1)
                    {
                        hasBlock = true;
                        break;
                    }
                }
                if (hasBlock)
                {
                    height = row + 1;
                }
            }
            return height;
        }

        public static bool check_operation_rotate()
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[check] check_operation_rotate");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            return false;
        }

        public static void fix_block(int[,,] block, int x, int y, int rotation)
        {
            for (int r = 0; r < 4; r++)
            {
                for (int c = 0; c < 4; c++)
                {
                    if (block[rotation, r, c] == 1)
                    {
                        Settings.board_result[y + r, x + c] = 1;
                        // Console.WriteLine($"check {y + r} {x + c}");
                    }
                }
            }
        }
    }
}
