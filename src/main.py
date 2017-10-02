import lemonator
import time

hw  = lemonator.lemonator(2)

def cheating(a):
    for i in range(a):
        time.sleep(1)
        hw.led_yellow.set(1)
        
if __name__=="__main__":
    keypad_input = hw.keypad.getc()
    if keypad_input == 'A':
        hw.sirup_pump.set(1)
        hw.sirup_valve.set(0)
        cheating(13)
        hw.sirup_pump.set(0)
        hw.sirup_valve.set(1)

        hw.water_pump.set(1)
        hw.water_valve.set(0)
        cheating(43)
        hw.water_pump.set(0)
        hw.water_valve.set(1)
        print('done')
        while(True):
            cheating(1)
            
