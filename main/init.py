import pygame # type: ignore
import csv
import config
from Leg import Leg
from Leg import Leg2Joints
from Joint import Joint
from Hexapod import Hexabot


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

def initialize_legs():
    legs = {}
    for leg_name in config.legs:
        position, joint_pins, lengths, offsets, inversions = config.legs[leg_name]
        joints = []

        for pin, offset, inverted in zip(joint_pins, offsets, inversions):
            joint = Joint(pin, offset, inverted)
            joints.append(joint)
        
        if joints[2].pin < 0:
            leg = Leg2Joints(position, joints, lengths)
        else:
            leg = Leg(position, joints, lengths)
        legs[leg_name] = leg

    return legs

def initialize_Hexabot():
    legs = initialize_legs()
    return Hexabot(legs)
