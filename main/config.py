from adafruit_servokit import ServoKit
import csv
from ikpy.chain import Chain
from ikpy.link import URDFLink

#Servo range
actuation_range = 125


# Initialize the ServoKit for a 16-channel Servo Hat
kit = ServoKit(channels=16)
for i in range(15):  
    kit.servo[i].actuation_range = actuation_range


# Link lengths 
L1 = 5  # Length of base to first vertical joint
L2 = 9  # Length of first vertical segment
L3 = 14  # Length of second vertical segment (foot)





# Create a kinematic chain using ikpy
# Define the lengths of the segments and create a robot arm (with 3 links)
robot = Chain(name='robot', links=[
    URDFLink(name='base', origin_translation=[L1, 0, 0], origin_orientation=[0, 0, 0], rotation=[0, 0, 1]),
    URDFLink(name='joint1', origin_translation=[L2, 0, 0], origin_orientation=[0, 0, 0], rotation=[0, 0, 1]),
    URDFLink(name='joint2', origin_translation=[L3, 0, 0], origin_orientation=[0, 0, 0], rotation=[0, 0, 1])
])

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