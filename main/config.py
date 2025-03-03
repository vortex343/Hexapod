#Servo range
actuation_range = 135

# Speaker pin
SPEAKER_PIN = 19  

# Link lengths 
L1 = 3
L2 = 10
L3 = 18.5

# Movement parameters
step_x = 6
step_y = 13
step_z = 13
step_count = 20
delay = 0.02

# CSV file path for Controller Mappings
csv_file_path = 'main/data/8bitDo.csv'

legs = {
    # 'leg_name':   [Position,      servo_pins,     lengths,        joint_offsets,      inverted]
    'front_left':   [[5.5, -4, 5],  [7,13,15],      [L1, L2, L3],   [300, 95, 350],    [False, True, False]],
    'front_right':  [[5.5, 4, 5],   [4,12,14],   [L1, L2, L3],   [15, 50, 140],      [False, False, True]],

    'middle_left':  [[0, -5, 5],    [6,11],         [L1, 24],   [65, 55 ],       [True, True]],
    'middle_right': [[0, 5, 5],     [3,10],       [L1, 24],   [65, 80],           [False, False]],

    'back_left':    [[-7, -4, 3], [5,9,0],        [L1, L2, L3],   [195, 85, 350],    [False, True, False]],
    'back_right':   [[-7, 4, 3],  [2,8,1],       [L1, L2, L3],   [120, 50, 140],     [False, False, True]]
}

