from adafruit_servokit import ServoKit
import csv
import pygame

def initialize_joystick():
    pygame.init()
    pygame.joystick.init()
    
    if pygame.joystick.get_count() == 0:
        raise RuntimeError("No joystick detected!")

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick

#Servo range
actuation_range = 125


# Initialize the ServoKit for a 16-channel Servo Hat
kit = ServoKit(channels=16)
for i in range(15):  
    kit.servo[i].actuation_range = actuation_range

# Link lengths 
L1 = 5
L2 = 9
L3 = 14

# Joint pos offset
offsets = {
    # 'joint_name': [x, y, z]
    'front_right': [0, 0, 0],
    'front_left': [0, 0, 0],
    'middle_right': [0, 0, 0],
    'middle_left': [0, 0, 0],
    'back_right': [0, 0, 0],
    'back_left': [0, 0, 0],
}

offset_angle_j1 = 330
offset_angle_j2 = 0
offset_angle_j3 = 30


# Initialize dictionaries to store button and axis mappings
button_mappings = {}
axis_mappings = {}

# Define the path to your CSV file
csv_file_path = '/home/elias/src/main/data/8bitDo.csv'

# Open and read the CSV file
with open(csv_file_path, mode='r') as file:
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