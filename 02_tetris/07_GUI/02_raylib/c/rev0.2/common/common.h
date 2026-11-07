#ifndef COMMON_H
#define COMMON_H

/*----------------------------*/
/* type */
/*----------------------------*/
typedef struct
{
    int x;
    int y;
    int rotation;
} common_pos_t;

enum common_key_number
{
    KEY_LEFT_NUM = 0,
    KEY_RIGHT_NUM,
    KEY_ROTATION_RIGHT_NUM,
    KEY_ROTATION_LEFT_NUM,
    KEY_DROP_NUM,
    KEY_HARD_DROP_NUM,
    KEY_GAME_FINISH_NUM,
    KEY_MAX
};

/*----------------------------*/
/* const */
/*----------------------------*/

/*----------------------------*/
/* public function */
/*----------------------------*/

#endif /* COMMON_H */