#include "led.h"
#include "delay.h"

volatile uint32_t dwt  = 0;
int main(void)
{
	led_init();
	dwt_init();
	
	while(1)
	{
		time_test_run();
		delay_ms(20000);
		LED_MCU_TOG;
		dwt = time_test_getms();
		
	}
}

