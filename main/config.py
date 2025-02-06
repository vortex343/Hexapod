from adafruit_servokit import ServoKit # type: ignore

kit = ServoKit(channels=16)

#Servo range
actuation_range = 125



# Link lengths 
L1 = 5
L2 = 10
L3 = 14


# Define the path to your CSV file
csv_file_path = '/home/elias/Hexapod/main/data/8bitDo.csv'

legs = {
    #TODO add the correct values
    # 'leg_name': [Position, servo_pins, lengths]
    'front_right': [[0, 0, 0], [13, 14, 15], [L1, L2, L3]],
    'front_left': [[0, 0, 0], [10, 11, 12], [L1, L2, L3]],
    'middle_left': [[0, 0, 0], [8, 9, -1], [L1, L2, L3]],
    'middle_right': [[0, 0, 0], [6, 7, -1], [L1, L2, L3]],
    'back_left': [[0, 0, 0], [3, 4, 5], [L1, L2, L3]],
    'back_right': [[0, 0, 0], [0, 1, 2], [L1, L2, L3]]
}

joint_offsets = {
    'j1': 320,
    'j2': 0,
    'j3': 40
}