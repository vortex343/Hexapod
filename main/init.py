import pygame
import csv
import config
from Leg import Leg
from Leg import Leg2Joints
from Joint import Joint
from Hexapod import Hexabot
from adafruit_servokit import ServoKit


def initialize_joystick():
    """
    Handles the initialization of the controller

    Returns:
        pygame.joystick.Joystick: the pygame joystick

    Raises:
        RuntimeError: If no joystick is detected.
    """
    pygame.init()
    pygame.joystick.init()
    
    if pygame.joystick.get_count() == 0:
        raise RuntimeError("No joystick detected!")

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    return joystick

def initialize_controller_mapping():
    """
    Gets the mappings from the controller CSV to map the name to the value.

    Returns:
        Tuple[Dict[str, int], Dict[str, int], Dict[str, int]]: A tuple containing:
            - button_mappings (Dict[str, int]): A dictionary where the keys are button names 
              (str) and the values are the corresponding button values (int).

            - axis_mappings (Dict[str, int]): A dictionary where the keys are button names 
              (str) and the values are the corresponding axis mappings (int).

            - hat_mappings (Dict[str, int]): A dictionary where the keys are button names 
              (str) and the values are the corresponding hat mappings (int).
    """

    button_mappings = {}
    axis_mappings = {}
    hat_mappings = {}

    with open(config.csv_file_path, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            button = row['Button']
            value = row['Value']
            axis = row['Axis']
            hat = row['Hat']
            
            # button mappings
            if value:
                button_mappings[button] = int(value)
            
            # axis mappings
            if axis:
                axis_mappings[button] = int(axis)

            # hat mappings (dpad)
            if hat:
                hat_mappings[button] = int(hat)

    return button_mappings, axis_mappings, hat_mappings

def initialize_legs():
    """
    Initializes the legs of the robot based on configuration data.

    This function creates `Leg` objects based on the configuration.

    Returns:
        Dict[str, Leg]: A dictionary mapping leg names (str) to their corresponding `Leg`
    
    Notes:
        - The `Leg` class represents a standard leg with multiple joints.
        - The `Leg2Joints` class is a subclass of `Leg`, representing a modified leg with only two joints.
    """
    legs = {}
    for leg_name in config.legs:
        kit = ServoKit(channels=16)

        # get data from config
        position, joint_pins, lengths, offsets, inversions = config.legs[leg_name]
        joints = []

        # create joints
        for pin, offset, inverted in zip(joint_pins, offsets, inversions):
            joint = Joint(offset, inverted, config.actuation_range, kit.servo[pin])
            joints.append(joint)
        
        # if there are only 2 joints create modified legs
        if joints[2].pin < 0:
            leg = Leg2Joints(position, joints, lengths)
        else:
            leg = Leg(position, joints, lengths)
        legs[leg_name] = leg

    return legs

def initialize_Hexabot():
    """
    Initializes a Hexabot robot by creating its legs and passing them to the Hexabot class.

    Returns:
        Hexabot: An instance of the `Hexabot` class, initialized with the robot's legs.
    """

    legs = initialize_legs()
    hexabot = Hexabot(legs)
    return hexabot