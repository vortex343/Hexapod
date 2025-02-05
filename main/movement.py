import config
import math


def map_axis_to_angle_inverse(value):
    return int((value - 1) * config.actuation_range/2 * -1)  

def map_axis_to_angle(value):
    return int((value + 1) * config.actuation_range/2)  

"""
the robot has 6 legs 
each leg has 3 servos except the middle legs which has 2 servos
the servos are connected to the servo hat
the servo hat has 16 channels
0-2: back right leg
3-5: back lef leg
6-7: middle right leg
8-9: middle left leg
10-12: front right leg
13-15: front left leg
"""


def move(throttleR, direction_x, direction_y):
    """ move the robot example"""
    
    test0 = map_axis_to_angle(throttleR)
    config.kit.servo[0].angle = test0 

    test1 = map_axis_to_angle(direction_y)
    config.kit.servo[1].angle = test1 

    test2 = map_axis_to_angle(direction_y)
    config.kit.servo[2].angle = test2 



def solve_ik_2d(target_position):
    # target_position = [x, y, z]
    x = target_position[0]
    y = target_position[1]
    z = target_position[2]
    


    # leg dimensions
    l2 = config.L2
    l3 = config.L3
    
    c = math.sqrt(y**2 + z**2)

    
    # Calculate angles
    angle3 = math.acos((l2**2 + l3**2 - c**2) / (2 * l2 * l3))

    temp1 = math.acos((l2**2 + c**2 - l3**2) / (2 * l2 * c))
    temp2 = math.atan(z / y)

    angle2 = temp1 - temp2

    return [0, math.degrees(angle2), math.degrees(angle3)]	



def translate_angles(angles):
    # Translate angles to servo angles
    offset_j2 = 0
    offset_j3 = 30


    angle2 = (angles[1] - offset_j2)%360
    angle3 = (angles[2] - offset_j3)%360

    if angle2 > config.actuation_range:
        raise ValueError("Angle 2 is out of range")
    
    if angle3 > config.actuation_range:
        raise ValueError("Angle 3 is out of range")
    
    return [0, angle2, angle3]


# Function to move servos based on IK angles
def move_arm(target_position):
    try:
        # Calculate joint angles
        angles = solve_ik_2d(target_position)
        # Translate angles to servo angles
        servo_angles = translate_angles(angles)
        # Move servos
        for i, angle in enumerate(servo_angles):
            config.kit.servo[i].angle = angle 


        print(f"Moved to target: {target_position} | Angles: {angles} | Servo Angles: {servo_angles}")
    except ValueError as e:
        print(f"Error: {e}")


