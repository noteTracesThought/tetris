#ifndef CYCLE_PROCESS_H
#define CYCLE_PROCESS_H

#include <stdbool.h>

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/

/*----------------------------*/
/* public function */
/*----------------------------*/
void cycle_process_init(void);
void cycle_process_10ms(void);
void cycle_process_50ms(void);
void cycle_process_100ms(void);
void cycle_process_500ms(void);
void cycle_process_1000ms(void);
bool pop_fall_event(void);

#endif /* CYCLE_PROCESS_H */