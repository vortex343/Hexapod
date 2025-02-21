#Servo range
actuation_range = 135

# Link lengths 
L1 = 6
L2 = 10
L3 = 18.5

# CSV file path for Controller Mappings
csv_file_path = 'main/data/8bitDo.csv'

legs = {
    # 'leg_name':   [Position,      servo_pins,     lengths,        joint_offsets,      inverted]
    'front_left':   [[5.5, -4, 5],  [5, 6, 7],      [L1, L2, L3],   [300, 120, 350],    [False, True, False]],
    'front_right':  [[5.5, 4, 5],   [13, 14, 15],   [L1, L2, L3],   [15, 10, 140],      [False, False, True]],

    'middle_left':  [[0, -5, 5],    [4, 3],         [L1, 25],   [65, 75 ],       [True, True]],
    'middle_right': [[0, 5, 5],     [12, 11],       [L1, 25],   [65, 75],           [False, False]],

    'back_left':    [[-7, -4, 3], [2, 1, 0],        [L1, L2, L3],   [195, 120, 350],    [False, True, False]],
    'back_right':   [[-7, 4, 3],  [10, 9, 8],       [L1, L2, L3],   [120, 10, 140],     [False, False, True]]
}

