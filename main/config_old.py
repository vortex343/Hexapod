#Servo range
actuation_range = 125

# Link lengths 
L1 = 2
L2 = 9
L3 = 14

# CSV file path for Controller Mappings
csv_file_path = 'main/data/8bitDo.csv'

legs = {
    # 'leg_name':   [Position,      servo_pins,     lengths,        joint_offsets,  inverted]
    'front_left':   [[5.5, -5, 4],  [5, 6, 7],      [L1, L2, L3],   [280, 35, 330],  [False, False, False]],
    'front_right':  [[5.5, 5, 4],   [13, 14, 15],   [L1, L2, L3],   [20, 90, 170], [False, True, True]],

    'middle_left':  [[0, -5, 4],    [3, 4],     [L1, L2, L3],   [215, 75], [False, True]],
    'middle_right': [[0, 5, 4],     [12, 11],   [L1, L2, L3],   [90, 50], [False, True]],

    'back_left':    [[-5.5, -5, 4], [2, 1, 0],      [L1, L2, L3],   [190, 35, 330], [False, False, False]],
    'back_right':   [[-5.5, 5, 4],  [10, 9, 8],     [L1, L2, L3],   [115, 90, 170], [False, True, True]]
}

