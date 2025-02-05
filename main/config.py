from adafruit_servokit import ServoKit
import csv
import pygame


#Servo range
actuation_range = 125

# Link lengths 
L1 = 5
L2 = 9
L3 = 14


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