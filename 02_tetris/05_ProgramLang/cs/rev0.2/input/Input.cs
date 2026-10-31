using System;

namespace Tetris
{
    public static class Input
    {
        public static int request_operation_rotate(char put_key, int[,,] block, int x, int y, int rotation)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[req] request_operation_rotate");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            if (put_key == Settings.KEY_ROTATION_LEFT)
            {
                rotation = request_operation_rotate_left(block, x, y, rotation);
            }
            if (put_key == Settings.KEY_ROTATION_RIGHT)
            {
                rotation = request_operation_rotate_right(block, x, y, rotation);
            }
            return rotation;
        }

        // ▼▼▼ ハードドロップ機能追加 ▼▼▼
        public static (int next_x, int next_y) get_next_position(char put_key, int[,,] block, int x, int y, int rotation)
        {
            // ▲▲▲ ハードドロップ機能追加 ▲▲▲
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[req] get_next_position");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲

            int next_x = x;
            int next_y = y;
            if (put_key == Settings.KEY_RIGHT)
            {
                next_x += 1;
            }
            else if (put_key == Settings.KEY_LEFT)
            {
                next_x -= 1;
            }
            else if (put_key == Settings.KEY_DROP)
            {
                next_y += 1;
            }
            // ▼▼▼ ハードドロップ機能追加 ▼▼▼
            else if (put_key == Settings.KEY_HARD_DROP)
            {
                next_y = Collision.execute_hard_drop(block, x, y, rotation);
            }
            // ▲▲▲ ハードドロップ機能追加 ▲▲▲
            else
            {
                // Do Nothing
            }

            return (next_x, next_y);
        }

        public static int request_operation_rotate_left(int[,,] block, int x, int y, int rotation)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[req] request_operation_rotate_left");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            int new_rotation = rotation - 1;
            if (new_rotation < 0)
            {
                new_rotation = 3;
            }

            int block_width = Block.get_block_width(block, new_rotation);
            int block_height = Block.get_block_height(block, new_rotation);
            if (x + block_width < 0)
            {
                new_rotation = rotation;
            }
            if (x + block_width > Settings.BOARD_SIZE_WIDTH)
            {
                new_rotation = rotation;
            }
            if (y + block_height < 0)
            {
                new_rotation = rotation;
            }
            if (y + block_height > Settings.BOARD_SIZE_HEIGHT)
            {
                new_rotation = rotation;
            }

            return new_rotation;
        }

        public static int request_operation_rotate_right(int[,,] block, int x, int y, int rotation)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            // Console.WriteLine("[req] request_operation_rotate_right");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            int new_rotation = rotation + 1;
            new_rotation = new_rotation % 4;

            int block_width = Block.get_block_width(block, new_rotation);
            int block_height = Block.get_block_height(block, new_rotation);
            if (x + block_width < 0)
            {
                new_rotation = rotation;
            }
            if (x + block_width >= Settings.BOARD_SIZE_WIDTH)
            {
                new_rotation = rotation;
            }
            if (y + block_height < 0)
            {
                new_rotation = rotation;
            }
            if (y + block_height >= Settings.BOARD_SIZE_HEIGHT)
            {
                new_rotation = rotation;
            }

            return new_rotation;
        }

        public static char getch_for_Linux()
        {
            // .NET(C#)には termios/tty に相当するAPIがないため、
            // クロスプラットフォームで利用できる Console.ReadKey(true) で代替する。
            ConsoleKeyInfo keyInfo = Console.ReadKey(true);
            return keyInfo.KeyChar;
        }
    }
}
