#ifndef CYCLE_CONFIG_H
#define CYCLE_CONFIG_H

#include "../cycle/cycle_types.h"

/*----------------------------*/
/* type */
/*----------------------------*/
typedef struct
{
    int    cid;            // 列挙型 ID
    int    cycle;          // 周期（ms）
    void   (*func)(void);  // 関数ポインタ（引数なし・戻り値なし）
} cycleconfig_cycle_t;


/*----------------------------*/
/* const */
/*----------------------------*/
extern const cycleconfig_cycle_t cycle_index[ID_MAX];

/*----------------------------*/
/* public function */
/*----------------------------*/

#endif /* CYCLE_CONFIG_H */