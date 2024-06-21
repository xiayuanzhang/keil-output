#ifndef _LED_H_
#define _LED_H_

#include "gd32f4xx.h"

#define RCU_MCULED  RCU_GPIOC
#define PORT_MCULED GPIOC
#define PIN_MCULED  GPIO_PIN_15


#define LED_MCU_ON  gpio_bit_write(PORT_MCULED,PIN_MCULED,RESET)
#define LED_MCU_OFF gpio_bit_write(PORT_MCULED,PIN_MCULED,SET)
#define LED_MCU_TOG gpio_bit_toggle(PORT_MCULED,PIN_MCULED)


void led_init(void);
void led_blink(void);




#endif // _LED_H_
