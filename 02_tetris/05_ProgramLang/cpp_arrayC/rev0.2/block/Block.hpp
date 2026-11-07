#ifndef BLOCK_HPP
#define BLOCK_HPP

/* テトロミノ1個分の形状データ [rotation][row][col] */
typedef int BlockShape[4][4][4];

namespace block {

/* block_map の1エントリ (Pythonの dict の key-value に相当) */
struct block_map_entry_t {
    char key;
    const int (*shape)[4][4];   /* BlockShape へのポインタ */
};

/* global (settings.py の block_map_key / block_map に相当、通常の固定長配列で実装) */
const int BLOCK_MAP_SIZE = 7;
extern char block_map_key[BLOCK_MAP_SIZE];
extern int  block_map_key_count;
extern block_map_entry_t block_map[BLOCK_MAP_SIZE];

void create_blocks();
const int (*get_block())[4][4];
int get_block_width(const int block[4][4][4], int rotation);
int get_block_height(const int block[4][4][4], int rotation);
bool check_operation_rotate();
void fix_block(const int block[4][4][4], int x, int y, int rotation);

} // namespace block

#endif // BLOCK_HPP
