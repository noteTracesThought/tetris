#ifndef INPUT_H
#define INPUT_H

#include "../common/common.h"
#include "../block/block.h"

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/

/*----------------------------*/
/* variable */
/*----------------------------*/

/*----------------------------*/
/* function section */
/*----------------------------*/

/*----------------------------*/
/* public function */
/*----------------------------*/
void init_input(void);
void request_operation_rotate(char put_key, common_pos_t *position);
void get_next_position(char put_key, const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t *position);
void input_putkey(void);
void set_putkey(char value);
char get_putkey(void);
void restore_input(void);

#endif /* INPUT_H */
