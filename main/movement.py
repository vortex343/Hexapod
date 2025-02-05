import config
import math

""" for testing purposes"""
def map_axis_to_angle_inverse(value):
    return int((value - 1) * config.actuation_range/2 * -1)  

""" for testing purposes"""
def map_axis_to_angle(value):
    return int((value + 1) * config.actuation_range/2)  

""" for testing purposes"""
def move(throttleR, direction_x, direction_y):
    """ move the robot example"""
    
    test0 = map_axis_to_angle(throttleR)
    config.kit.servo[0].angle = test0 

    test1 = map_axis_to_angle(direction_y)
    config.kit.servo[1].angle = test1 

    test2 = map_axis_to_angle(direction_y)
    config.kit.servo[2].angle = test2 



""" for testing purposes"""
def solve_ik_2d(target_position):

    # relative target_position = [x, y, z]
    y = target_position[1] + config.offset_j2_y
    z = target_position[2] + config.offset_j2_z


    # leg dimensions
    l2 = config.L2
    l3 = config.L3
    
    c = math.sqrt(y**2 + z**2)

    
    # Calculate angles
    angle3 = math.acos((l2**2 + l3**2 - c**2) / (2 * l2 * l3))

    temp1 = math.acos((l2**2 + c**2 - l3**2) / (2 * l2 * c))
    temp2 = math.atan2(z , y)
    angle2 = temp1 - temp2

    return [0, math.degrees(angle2), math.degrees(angle3)]	


def solve_ik_3d(target_position):

    # relative target_position = [x, y, z]
    x = target_position[0] + config.offset_j1_x
    y = target_position[1] + config.offset_j2_y
    z = -(target_position[2] + config.offset_j2_z)


    # leg dimensions
    l2 = config.L2
    l3 = config.L3
    
    c = math.sqrt(x**2 + y**2)


    # Calculate angles
    angle1 = math.atan2(x, y)

    angle3 = math.acos((l2**2 + l3**2 - c**2) / (2 * l2 * l3))

    temp1 = math.acos((l2**2 + c**2 - l3**2) / (2 * l2 * c))
    temp2 = math.atan2(z , y)
    angle2 = temp1 - temp2


    return [math.degrees(angle1), math.degrees(angle2), math.degrees(angle3)]


def translate_angles(angles):
    # Translate angles to servo angles
    angle1 = (angles[0] - config.offset_angle_j1 + 360)%360
    angle2 = (angles[1] - config.offset_angle_j2 + 360)%360
    angle3 = (angles[2] - config.offset_angle_j3 + 360)%360

    if angle1 > config.actuation_range:
        raise ValueError("Angle 1 is out of range")
    
    if angle2 > config.actuation_range:
        raise ValueError("Angle 2 is out of range")
    
    if angle3 > config.actuation_range:
        raise ValueError("Angle 3 is out of range")
    
    return [angle1, angle2, angle3]


def move_arm(target_position):
    
    angles = solve_ik_3d(target_position)
    servo_angles = translate_angles(angles)


    # Move servos
    for i, angle in enumerate(servo_angles):
        config.kit.servo[i].angle = angle 

    print(f"Moved to target: {target_position} | Angles: {angles} | Servo Angles: {servo_angles}")


