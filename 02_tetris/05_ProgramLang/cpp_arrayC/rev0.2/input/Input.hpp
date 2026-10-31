#ifndef INPUT_HPP
#define INPUT_HPP

namespace input {

/* ▼▼▼ ハードドロップ機能追加 ▼▼▼ */
int request_operation_rotate(char put_key, const int block[4][4][4], int x, int y, int rotation);
void get_next_position(char put_key, const int block[4][4][4], int x, int y, int rotation, int *next_x, int *next_y);
/* ▲▲▲ ハードドロップ機能追加 ▲▲▲ */
int request_operation_rotate_left(const int block[4][4][4], int x, int y, int rotation);
int request_operation_rotate_right(const int block[4][4][4], int x, int y, int rotation);
char getch_for_Linux();

} // namespace input

#endif // INPUT_HPP
