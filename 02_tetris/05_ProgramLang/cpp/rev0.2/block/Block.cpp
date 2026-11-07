#include <cstdlib>
#include <algorithm>
#include "../block/Block.hpp"
#include "../Settings.hpp"

namespace block {

/* 各ブロックは [rotation(TOP,RIGHT,BOTTOM,LEFT)][row][col] の順で定義 */
static const BlockShape I = {{
    {{{1,1,1,1},{0,0,0,0},{0,0,0,0},{0,0,0,0}}},
    {{{0,0,0,1},{0,0,0,1},{0,0,0,1},{0,0,0,1}}},
    {{{0,0,0,0},{0,0,0,0},{0,0,0,0},{1,1,1,1}}},
    {{{1,0,0,0},{1,0,0,0},{1,0,0,0},{1,0,0,0}}}
}};

static const BlockShape J = {{
    {{{0,1,1,1},{0,0,0,1},{0,0,0,0},{0,0,0,0}}},
    {{{0,0,0,0},{0,0,0,1},{0,0,0,1},{0,0,1,1}}},
    {{{0,0,0,0},{0,0,0,0},{1,0,0,0},{1,1,1,0}}},
    {{{1,1,0,0},{1,0,0,0},{1,0,0,0},{0,0,0,0}}}
}};

static const BlockShape L = {{
    {{{1,1,1,0},{1,0,0,0},{0,0,0,0},{0,0,0,0}}},
    {{{0,0,1,1},{0,0,0,1},{0,0,0,1},{0,0,0,0}}},
    {{{0,0,0,0},{0,0,0,0},{0,0,0,1},{0,1,1,1}}},
    {{{0,0,0,0},{1,0,0,0},{1,0,0,0},{1,1,0,0}}}
}};

static const BlockShape S = {{
    {{{0,0,1,1},{0,1,1,0},{0,0,0,0},{0,0,0,0}}},
    {{{0,0,0,0},{0,0,1,0},{0,0,1,1},{0,0,0,1}}},
    {{{0,0,0,0},{0,0,0,0},{0,1,1,0},{1,1,0,0}}},
    {{{1,0,0,0},{1,1,0,0},{0,1,0,0},{0,0,0,0}}}
}};

static const BlockShape Z = {{
    {{{0,1,1,0},{0,0,1,1},{0,0,0,0},{0,0,0,0}}},
    {{{0,0,0,0},{0,0,0,1},{0,0,1,1},{0,0,1,0}}},
    {{{0,0,0,0},{0,0,0,0},{1,1,0,0},{0,1,1,0}}},
    {{{0,1,0,0},{1,1,0,0},{1,0,0,0},{0,0,0,0}}}
}};

static const BlockShape O = {{
    {{{0,0,1,1},{0,0,1,1},{0,0,0,0},{0,0,0,0}}},
    {{{0,0,0,0},{0,0,0,0},{0,0,1,1},{0,0,1,1}}},
    {{{0,0,0,0},{0,0,0,0},{1,1,0,0},{1,1,0,0}}},
    {{{1,1,0,0},{1,1,0,0},{0,0,0,0},{0,0,0,0}}}
}};

static const BlockShape T = {{
    {{{0,0,1,0},{0,1,1,1},{0,0,0,0},{0,0,0,0}}},
    {{{0,0,0,0},{0,0,1,0},{0,0,1,1},{0,0,1,0}}},
    {{{0,0,0,0},{0,0,0,0},{1,1,1,0},{0,1,0,0}}},
    {{{0,1,0,0},{1,1,0,0},{0,1,0,0},{0,0,0,0}}}
}};

/* global (settings.py の block_map_key / block_map に相当) */
std::vector<char> block_map_key;
std::vector<block_map_entry_t> block_map;

void create_blocks()
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[init] create_blocks" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    block_map_key.clear();
    block_map.clear();

    block_map.push_back({'I', &I});
    block_map.push_back({'J', &J});
    block_map.push_back({'L', &L});
    block_map.push_back({'S', &S});
    block_map.push_back({'Z', &Z});
    block_map.push_back({'O', &O});
    block_map.push_back({'T', &T});

    for (const auto &entry : block_map) {
        block_map_key.push_back(entry.key);
    }

    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    std::srand(1234567);
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
}

const BlockShape &get_block()
{
    int index = std::rand() % static_cast<int>(block_map_key.size());
    char selected_key = block_map_key[index];

    for (const auto &entry : block_map) {
        if (entry.key == selected_key) {
            return *entry.shape;
        }
    }
    return *block_map.front().shape;
}

int get_block_width(const BlockShape &block, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[check] get_block_width" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int width = 0;
    for (const auto &row : block[rotation]) {
        for (std::size_t col = 0; col < row.size(); ++col) {
            if (row[col] == 1) {
                width = std::max(width, static_cast<int>(col) + 1);
            }
        }
    }
    return width;
}

int get_block_height(const BlockShape &block, int rotation)
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[check] get_block_height" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    int height = 0;
    for (std::size_t row = 0; row < block[rotation].size(); ++row) {
        bool has_block = false;
        for (int cell : block[rotation][row]) {
            if (cell == 1) {
                has_block = true;
                break;
            }
        }
        if (has_block) {
            height = static_cast<int>(row) + 1;
        }
    }
    return height;
}

bool check_operation_rotate()
{
    /* ▼▼▼ 処理速度計測（10万回） ▼▼▼ */
    // std::cout << "[check] check_operation_rotate" << std::endl;
    /* ▲▲▲ 処理速度計測（10万回） ▲▲▲ */
    return false;
}

void fix_block(const BlockShape &block, int x, int y, int rotation)
{
    for (std::size_t r = 0; r < block[rotation].size(); ++r) {
        for (std::size_t c = 0; c < block[rotation][r].size(); ++c) {
            if (block[rotation][r][c] == 1) {
                settings::board_result[y + r][x + c] = 1;
                // std::cout << "check " << y + r << " " << x + c << std::endl;
            }
        }
    }
}

} // namespace block
