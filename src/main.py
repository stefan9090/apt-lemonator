import lemonator
import time

hw  = lemonator.lemonator(2)
heater = False

def keep_temp(d, temp):
    global heater

    timer = 0
    while timer < d:
        timer += 0.2
        time.sleep(0.2)
        if not heater and hw.temperature.read_mc() < temp - 0.5:
            heater = True
            hw.heater.set(1)
        elif heater and hw.temperature.read_mc() > temp + 0.5:
            heater = False
            hw.heater.set(0)

if __name__=="__main__":
    while True:
        keypad_input = hw.keypad.getc()
        if keypad_input == 'A':
            hw.sirup_pump.set(1)
            hw.sirup_valve.set(0)
            hw.water_pump.set(1)
            hw.water_valve.set(0)
            keep_temp(13, 30)
            hw.sirup_pump.set(0)
            hw.sirup_valve.set(1)
            keep_temp(30, 30)
            hw.water_pump.set(0)
            hw.water_valve.set(1)
            keep_temp(20, 30)
            print('done')
