#ifndef BLOCK_HPP
#define BLOCK_HPP

#include <array>
#include <vector>

namespace block {

/* テトロミノ1個分の形状データ [rotation][row][col] */
using BlockShape = std::array<std::array<std::array<int, 4>, 4>, 4>;

/* block_map の1エントリ (Pythonの dict の key-value に相当) */
struct BlockMapEntry {
    char key;
    const BlockShape *shape;
};

/* global (settings.py の block_map_key / block_map に相当) */
extern std::vector<char> block_map_key;
extern std::vector<BlockMapEntry> block_map;

void create_blocks();
const BlockShape &get_block();
int get_block_width(const BlockShape &block, int rotation);
int get_block_height(const BlockShape &block, int rotation);
bool check_operation_rotate();
void fix_block(const BlockShape &block, int x, int y, int rotation);

} // namespace block

#endif // BLOCK_HPP
