using System;
using System.Diagnostics;

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
    public static class Program
    {
        public static void Main(string[] args)
        {
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            Stopwatch stopwatch = Stopwatch.StartNew();
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            Game.power_on_game();
            // ▼▼▼ 処理速度計測（10万回） ▼▼▼
            stopwatch.Stop();
            Console.WriteLine($"time = {stopwatch.Elapsed.TotalMilliseconds}ms");
            // ▲▲▲ 処理速度計測（10万回） ▲▲▲
            Console.WriteLine("[task] power off");
        }
    }
}
