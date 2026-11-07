#include "../cycle/cycle_config.h"
#include "../cycle/cycle_process.h"

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/
// const CycleIndex_t cycle_index[ID_MAX] =
// {
// /*   cid,     cycle, func */
//     {ID_1,    1U,     NULL},
//     {ID_2,    2U,     NULL},
//     {ID_4,    4U,     NULL},
//     {ID_10,   10U,    cycle_process_10ms},
//     {ID_50,   50U,    cycle_process_50ms},
//     {ID_100,  100U,   cycle_process_100ms},
//     {ID_500,  500U,   cycle_process_500ms},
//     {ID_1000, 1000U,  cycle_process_1000ms}
// };
const cycleconfig_cycle_t cycle_index[ID_MAX] =
{
/*   cid,     cycle, func */
    {ID_1000, 1000U,  cycle_process_1000ms}
};
/*----------------------------*/
/* variable */
/*----------------------------*/

/*----------------------------*/
/* function section */
/*----------------------------*/

/*----------------------------*/
/* public function */
/*----------------------------*/
