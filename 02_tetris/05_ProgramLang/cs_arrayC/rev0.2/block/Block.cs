using System;

namespace Tetris
{
    /// <summary>
    /// block_map の1エントリ (Pythonの dict の key-value に相当、通常の配列で実装)
    /// </summary>
    public struct block_map_entry_t
    {
        public char key;
        public int[,,] shape;
    }

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

        // global (settings.py の block_map_key / block_map に相当、通常の固定長配列で実装)
        public const int BLOCK_MAP_SIZE = 7;
        public static char[] block_map_key = new char[BLOCK_MAP_SIZE];
        public static int block_map_key_count = 0;
        public static block_map_entry_t[] block_map = new block_map_entry_t[BLOCK_MAP_SIZE];

        // ▼▼▼ 処理速度計測（10万回） ▼▼▼
        private static readonly Random random = new Random(1234567);
        // ▲▲▲ 処理速度計測（10万回） ▲▲▲

        public static void create_blocks()
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[init] create_blocks");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            block_map_key_count = 0;

            block_map[0] = new block_map_entry_t { key = 'I', shape = I };
            block_map[1] = new block_map_entry_t { key = 'J', shape = J };
            block_map[2] = new block_map_entry_t { key = 'L', shape = L };
            block_map[3] = new block_map_entry_t { key = 'S', shape = S };
            block_map[4] = new block_map_entry_t { key = 'Z', shape = Z };
            block_map[5] = new block_map_entry_t { key = 'O', shape = O };
            block_map[6] = new block_map_entry_t { key = 'T', shape = T };

            for (int i = 0; i < BLOCK_MAP_SIZE; i++)
            {
                block_map_key[block_map_key_count++] = block_map[i].key;
            }
        }

        public static int[,,] get_block()
        {
            int index = random.Next(block_map_key_count);
            char selected_key = block_map_key[index];

            for (int i = 0; i < BLOCK_MAP_SIZE; i++)
            {
                if (block_map[i].key == selected_key)
                {
                    return block_map[i].shape;
                }
            }
            return null;
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
