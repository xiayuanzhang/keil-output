/**
 * \copyright Copyright (c) 2024  xxxcompany
 * \file delay.c
 * \date 2024-06-14
 * \author fyuan (xxx@email.com)
 * 
 * \brief 
 * 该文件使用 DWT 计时器来完成us,ms级延时. 并且提供函数运行时间测量函数.
 * 
 * DWT计时器和systick一样,是cortex-m内核的寄存器,所以不受限于芯片
 *
 * DWT计时器的时钟频率为系统时钟频率
 */
#include "delay.h"

static uint32_t DWT_TICK_MS = 0;
static uint32_t DWT_TICK_US = 0;
static uint32_t DWT_MAXTIME_MS = 0;
static uint32_t DWT_MAXTIME_US = 0;

//不能使用0xffffffff计算最大值, 要留有足够的时间余量, 才能够使while判断正确
//如果出现程序一直在delay函数中的delay中等到, 应该将该值继续减小.
const uint32_t MAX_TICK = 0xF0000000;

void dwt_init(void)
{
    /* 使能DWT外设 */
    DEM_CR |= (uint32_t)DEM_CR_TRCENA;                

    /* DWT CYCCNT寄存器计数清0 */
    DWT_CYCCNT = (uint32_t)0u;

    /* 使能Cortex-M DWT CYCCNT寄存器 */
    DWT_CR |= (uint32_t)DWT_CR_CYCCNTENA;
	
    DWT_TICK_MS = DWT_TICK / 1000;
    DWT_TICK_US = DWT_TICK / 1000000;
    DWT_MAXTIME_MS = MAX_TICK / DWT_TICK_MS;
    DWT_MAXTIME_US = MAX_TICK / DWT_TICK_US;
}



void delay_us(uint32_t us)
{
    uint32_t count = 0,start = 0,ticks = 0;
    if(us > DWT_MAXTIME_US){
        count = us / DWT_MAXTIME_US;
        us = us % DWT_MAXTIME_US;
    }
    for(uint32_t i = 0; i < count; i++){
        start = DWT_CYCCNT;
        while(DWT_CYCCNT - start < MAX_TICK);
    }
    start = DWT_CYCCNT;
    ticks = us * DWT_TICK_US;
    while(DWT_CYCCNT - start < ticks);
}


void delay_ms(uint32_t ms)
{
    uint32_t count = 0,start = 0,ticks = 0;
    if(ms > DWT_MAXTIME_MS){
        count = ms / DWT_MAXTIME_MS;
        ms = ms % DWT_MAXTIME_MS;
    }
    for(uint32_t i = 0; i < count; i++){
        start = DWT_CYCCNT;
        while(DWT_CYCCNT - start < MAX_TICK);
    }
    start = DWT_CYCCNT;
    ticks = ms * DWT_TICK_MS;
    while(DWT_CYCCNT - start < ticks);
}


void time_test_run()
{
    DWT_CYCCNT = 0;
}


uint32_t time_test_gettick()
{
    return DWT_CYCCNT;
}

uint32_t time_test_getus()
{
    return DWT_CYCCNT / DWT_TICK_US;
}

uint32_t time_test_getms()
{
    return DWT_CYCCNT / DWT_TICK_MS;
}




