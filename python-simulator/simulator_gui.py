import sys
import os
import time
import pygame
from pygame.locals import *

import threading

"""
Creates a second thread to run the given simulator in, this makes it so the gui and simulation works even if the main thread is waiting for an event or time delay
"""
class simulator_thread(threading.Thread):
    # Initialize the thread  and save the simulator to use
    def __init__(self, threadID, name, simulator):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.simulator = simulator

    # Runs the thread where the gui and simulator get updated
    def run(self):
        while True:
            self.simulator.simulator.update()
            self.simulator.update()
"""
Creates a gui for the simulator which holds all the grapical elements and handles keypad input
"""
class simulator_gui(object):
    # Initializes pygame and creates the various elements of the simulator
    def __init__(self, simulator):
        pygame.init()

        self.simulator = simulator

        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.button_font = pygame.font.Font(pygame.font.get_default_font(), 50)

        self.buttons = ['1', '2', '3', 'A', '4', '5', '6', 'B', '7', '8', '9', 'C', '*','0', '#', 'D']
        self.lcd_text1 = "Test string 1"
        self.lcd_text2 = "Test string 2"

        self.size = self.width, self.height = 620, 480
        self.background = 255, 255, 255

        self.screen = pygame.display.set_mode(self.size)

        self.leds = {"yellow" : False,
                     "green" : False}

        self.key = None

        self.thread = simulator_thread(1, "simulator-thread", self)
        self.thread.start()

    # Sets the yellow led to on or off
    def set_yellow_led(self, value):
        self.leds["yellow"] = value

    # Sets the yellow led to on or off
    def set_green_led(self, value):
        self.leds["green"] = value

    # Waits untill the gui thread received a keypad input and then returns the value of the keypad
    def get_keypad(self):
        while self.key == None:
            time.sleep(0.02)

        key = self.key
        self.key = None
        return key

    # Renders a tank on the gui at the given position with a color and filled with value as a percentage
    def draw_tank(self, x, y, color, value):
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 1, 130))
        pygame.draw.rect(self.screen, (0, 0, 0), (x + 49, y, 1, 130))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y + 130, 50, 1))

        a = value / 100 * 130
        pygame.draw.rect(self.screen, color, (x + 1, y + (130 - a), 48, a))

        self.screen.blit(self.font.render("%3.1f %%" % (value,), 1, (0, 0, 0)), (x, y + 130))

    # Renders the heater at the given position
    def draw_heater(self, x, y):
        if self.simulator.heater_state:
            pygame.draw.rect(self.screen, (255, 255, 0), (x, y, 60, 10))
        else:
            pygame.draw.rect(self.screen, (60, 60, 60), (x, y, 60, 10))

        self.screen.blit(self.font.render("%3.1f mC" % (self.simulator.read_real_temp(),), 1, (0, 0, 0)), (x, y + 10))

    # Renders the keypad on the given location
    def draw_keypad(self, x, y):
        for i in range(len(self.buttons)):
            color = (0, 162, 230)
            if (self.buttons[i] > '9' or self.buttons[i] < '0'):
                color = (255, 0, 0)
            pygame.draw.rect(self.screen, color, (x + (i % 4 * 70), y + (i // 4 * 70), 64, 64))
            self.screen.blit(self.button_font.render(self.buttons[i], 1, (255, 255, 255)), (x + (i % 4 * 70) + 15, y + (i // 4 * 70) + 10))

    # Checks for keypad input with they keypad at x, y and pos the mouse position
    def handle_keypad(self, x, y, pos):
        mx, my = pos
        for i in range(len(self.buttons)):
            if mx >=  x + (i % 4 * 70) and mx <= x + (i % 4 * 70) + 64 and my >= y + (i // 4 * 70) and my <= y + (i // 4 * 70) + 64:
                self.handle_button(self.buttons[i])

    # Callback for if a button on the keypad is pressed
    def handle_button(self, button):
        self.key = button

    # Draws a led with color at the given position
    def draw_led(self, x, y, color, value):
        pygame.draw.circle(self.screen, (0, 0, 0), (x + 5, y + 1), 10)
        if value:
            pygame.draw.circle(self.screen, color, (x + 5, y + 1), 9)
        else:
            r, g, b = color
            pygame.draw.circle(self.screen, (r // 2, g // 2, b // 2), (x + 5, y + 1), 9)

    # Draws the lcd on the given position
    def draw_lcd(self, x, y):
        pygame.draw.rect(self.screen, (48, 136, 32), (x, y, 350, 80))
        self.screen.blit(self.font.render(self.lcd_text1, 1, (0, 0, 0)), (x + 10, y + 10))
        self.screen.blit(self.font.render(self.lcd_text2, 1, (0, 0, 0)), (x + 10, y + 50))

    # Draws a toggle switch at the given position to remove or place the cup
    def draw_toggle_switch(self, x, y):
        color = (255, 0, 0)
        if (self.simulator.cup_present):
            color = (0, 255, 0)
        pygame.draw.rect(self.screen, color, (x, y, 60, 20))

        if (self.simulator.cup_present):
            pygame.draw.rect(self.screen, (0, 0, 0), (x + 40, y, 20, 20))
            pygame.draw.rect(self.screen, (200, 200, 200), (x + 41, y + 1, 18, 18))
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 20, 20))
            pygame.draw.rect(self.screen, (200, 200, 200), (x + 1, y + 1, 18, 18))

    # Checks if the toggle switch has been pressed and updates the cup present in the simulator
    def handle_toggle_switch(self, x, y, pos):
        mx, my = pos
        if mx >= x and mx <= x + 60 and my >= y and my <= y + 20:
            self.simulator.set_cup(not self.simulator.get_cup())
            if not self.simulator.get_cup():
                self.simulator.set_liquids_level(0)

    # Handle GUI Events and render a frame
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: os._exit(0)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.handle_keypad(330, 110, pos)
                self.handle_toggle_switch(10, 200, pos)

        self.screen.fill(self.background)

        self.draw_tank(10, 10, (255, 0, 0), 100)
        self.draw_tank(160, 10, (122, 255, 245), 100)

        if self.simulator.cup_present:
            self.draw_tank(80, 200, (255, 0, 255), (89 - self.simulator.read_real_mm()) * 2)

        self.draw_heater(75, 360)

        self.draw_led(20, 240, (255, 255, 0), self.leds["yellow"])
        self.draw_led(50, 240, (0, 255, 0), self.leds["green"])

        self.draw_led(70, 100, (255, 0, 0), self.simulator.sirup_pump_state)
        self.draw_led(130, 100, (255, 0, 0), self.simulator.water_pump_state)
        self.draw_led(70, 130, (255, 0, 0), self.simulator.sirup_valve_state)
        self.draw_led(130, 130, (255, 0, 0), self.simulator.water_valve_state)

        self.draw_keypad(330, 110)
        self.draw_toggle_switch(10, 200)

        self.draw_lcd(260, 10)

        self.screen.blit(self.font.render("%3.2f mm" % (self.simulator.read_real_mm(),), 1, (0, 0, 0)), (180, 180))

        pygame.display.flip()
