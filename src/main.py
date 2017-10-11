import lemonator
import time

hw  = lemonator.lemonator(2)
heater = False

empty_cup = 89
full_cup = 50

def keep_temp(d, temp):
    global heater

    timer = 0
    while timer < d:
        timer += 0.8
        time.sleep(0.8)
        if not heater and hw.temperature.read_mc() + 700 < temp - 500:
            heater = True
            hw.heater.set(1)
        elif heater and hw.temperature.read_mc() + 700 > temp + 500:
            heater = False
            hw.heater.set(0)

def calculate_sirup_level(sirup_value, water_value):
    return empty_cup - (empty_cup - full_cup) * (1 / (sirup_value + water_value)) * sirup_value * 2

def fill_cup(sirup_value, water_value):
    global heater

    hw.sirup_pump.set(1)
    hw.sirup_valve.set(0)
    hw.water_pump.set(1)
    hw.water_valve.set(0)

    sirup_level = calculate_sirup_level(sirup_value, water_value)
    if sirup_value > water_value:
        sirup_level = calculate_sirup_level(water_value, sirup_value)

    while hw.distance.read_mm() > sirup_level:
        keep_temp(0.2, 22000)

    if sirup_value < water_value:
        hw.sirup_pump.set(0)
        hw.sirup_valve.set(1)
    else:
        hw.water_pump.set(0)
        hw.water_valve.set(1)

    while hw.distance.read_mm() > full_cup:
        keep_temp(0.2, 22000)

    if sirup_value < water_value:
        hw.water_pump.set(0)
        hw.water_valve.set(1)
    else:
        hw.sirup_pump.set(0)
        hw.sirup_valve.set(1)

    hw.heater.set(0)
    heater = False

if __name__=="__main__":
    while True:
        keypad_input = hw.keypad.getc()
        if keypad_input == 'A':
            fill_cup(1, 10)
        if keypad_input == 'B':
            fill_cup(2, 10)
        if keypad_input == 'C':
            fill_cup(1, 20)
        if keypad_input == 'D':
            fill_cup(1, 3)
        if keypad_input == '*':
            fill_cup(3, 1)
