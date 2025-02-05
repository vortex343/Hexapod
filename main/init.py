import pygame
import csv
import config

def initialize_joystick():
    pygame.init()
    pygame.joystick.init()
    
    if pygame.joystick.get_count() == 0:
        raise RuntimeError("No joystick detected!")

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick

def initialize_button_mapping():
    button_mappings = {}
    axis_mappings = {}

    with open(config.csv_file_path, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            button = row['Button']
            value = row['Value']
            axis = row['Axis']
            
            # Store button mappings
            if value:
                button_mappings[button] = int(value)
            
            # Store axis mappings
            if axis:
                axis_mappings[button] = int(axis)

    return button_mappings, axis_mappings