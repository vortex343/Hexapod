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
    # 'leg_name':   [Position,      servo_pins,     lengths,        joint_offsets,  invertecd]
    'front_left':   [[5.5, -5, 4],  [5, 6, 7],      [L1, L2, L3],   [0, 0, 0],      [False, False, False]],
    'front_right':  [[5.5, 5, 4],   [13, 14, 15],   [L1, L2, L3],   [340, 325, 45], [False, True, True]],
    'middle_left':  [[0, -5, 4],    [3, 4, -1],     [L1, L2, L3],   [0, 0, 0],      [True, False, False]],
    'middle_right': [[0, 5, 4],     [12, 11, -1],   [L1, L2, L3],   [0, 0, 0],      [False, True, True]],
    'back_left':    [[-5.5, -5, 4], [2, 1, 0],      [L1, L2, L3],   [0, 0, 0],      [True, False, False]],
    'back_right':   [[-5.5, 5, 4],  [10, 9, 8],     [L1, L2, L3],   [0, 0, 0],      [False, True, True]]
}

