#ifndef GAME_H
#define GAME_H

#include <stdbool.h>
#include "../common/common.h"
#include "../block/block.h"
#include "../board/board.h"

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
void power_on_game(void);
void init_game(void);
bool is_game_over(char put_key);
void set_update_view(bool value);
void is_update_view(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position);
void update_view_gui(const int block[ROUTATION_COUNT][BLOCK_SIZE_HEIGHT][BLOCK_SIZE_WIDTH], common_pos_t position);
void time_sleep(double seconds);

#endif /* GAME_H */
