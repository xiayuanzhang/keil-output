#include "led.h"

void led_init(void)
{
    rcu_periph_clock_enable(RCU_MCULED);
    gpio_mode_set(PORT_MCULED,GPIO_MODE_OUTPUT,GPIO_PUPD_NONE,PIN_MCULED);
	gpio_output_options_set(PORT_MCULED,GPIO_OTYPE_PP,GPIO_OSPEED_50MHZ,PIN_MCULED);
    LED_MCU_OFF;
}


void led_blink(void)
{
    LED_MCU_TOG;
}

