#include "../cycle/cycle_process.h"
#include "../cycle/cycle_types.h"

/*----------------------------*/
/* type */
/*----------------------------*/

/*----------------------------*/
/* const */
/*----------------------------*/

/*----------------------------*/
/* variable */
/*----------------------------*/
static bool need_render_fall[ID_MAX];

/*----------------------------*/
/* function section */
/*----------------------------*/
void set_need_fall(int index);

/*----------------------------*/
/* public function */
/*----------------------------*/
void cycle_process_init(void)
{
    for(int cnt = 0; cnt < ID_MAX; cnt++)
    {
        need_render_fall[cnt] = false;
    }
}
void cycle_process_10ms(void)
{
    /* printf("[proc] process_10ms\n") */
    return;
}
void cycle_process_50ms(void)
{
    /* printf("[proc] process_50ms\n") */
    return;
}
void cycle_process_100ms(void)
{
    /* printf("[proc] process_100ms\n") */
    return;
}
void cycle_process_500ms(void)
{
    /* printf("[proc] process_500ms\n") */
    return;
}
void cycle_process_1000ms(void)
{
    /* printf("[proc] process_1000ms\n") */
    set_need_fall(ID_1000);
    return;
}

bool pop_fall_event(void)
{
    /* 落下・再描画フラグを取得し、リセットする */

    int index;
    index = ID_1000;
    if(need_render_fall[index] == true)
    {
        need_render_fall[index] = false;
        return true;
    }
    return false;
}

/*----------------------------*/
/* private function */
/*----------------------------*/
void set_need_fall(int index)
{
    /* 落下・再描画フラグを有効にする */
    need_render_fall[index] = true;
}
