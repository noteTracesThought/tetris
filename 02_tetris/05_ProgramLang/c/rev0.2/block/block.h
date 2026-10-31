#ifndef BLOCK_H
#define BLOCK_H

#include <stdbool.h>

/* テトロミノ1個分の形状データ [rotation][row][col] */
typedef int BlockShape[4][4][4];

/* block_map の1エントリ (Pythonの dict の key-value に相当) */
typedef struct {
    char key;
    const int (*shape)[4][4];   /* BlockShape へのポインタ */
} BlockMapEntry;

/* global (settings.py の block_map_key / block_map に相当) */
#define BLOCK_MAP_SIZE 7
extern char block_map_key[BLOCK_MAP_SIZE];
extern int  block_map_key_count;
extern BlockMapEntry block_map[BLOCK_MAP_SIZE];

void create_blocks(void);
const int (*get_block(void))[4][4];
int get_block_width(const int block[4][4][4], int rotation);
int get_block_height(const int block[4][4][4], int rotation);
bool check_operation_rotate(void);
void fix_block(const int block[4][4][4], int x, int y, int rotation);

#endif /* BLOCK_H */
