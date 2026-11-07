#ifndef SETTINGS_H
#define SETTINGS_H

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/
/* OS */
#define WINDOWS             "Windows"
#define LINUX               "Linux"
#define OS_ENVIROMENT       LINUX       /* selection WINDOWS or LINUX */

/* keyboard */
#define KEY_HARD_DROP       'h'         /* 一気に下へ落とす */
#define KEY_DROP            ' '         /* 下へ加速 */
#define KEY_LEFT            's'         /* 左へ移動 */
#define KEY_RIGHT           'd'         /* 右へ移動 */
#define KEY_ROTATION_RIGHT  'r'         /* ブロックを右回転 */
#define KEY_ROTATION_LEFT   'w'         /* ブロックを左回転 */
#define KEY_GAME_FINISH     'q'         /* ゲームを強制終了させる */
/* ----------------------------------------------- */

/* board */
#define BOARD_SIZE_HEIGHT   20          /* board height */
#define BOARD_SIZE_WIDTH    10          /* board width */

/*----------------------------*/
/* variable */
/*----------------------------*/
extern const double SCORE_MULTIPLIER[5]; /* 設計変更対応（スコア倍率変更） */

/*----------------------------*/
/* function section */
/*----------------------------*/

/*----------------------------*/
/* public function */
/*----------------------------*/

#endif /* SETTINGS_H */
