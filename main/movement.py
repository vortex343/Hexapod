import config
import math


def solve_ik_3d(target_position, arm):
    # relative target_position = [x, y, z]
    offset = config.offsets[arm]
    x = target_position[0] + offset[0]
    y = target_position[1] + offset[1]
    z = -(target_position[2] + offset[2])

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

def move_arm(servo_angles, arm):
    # Move the arm to the target position
    for i in range(3):
        if config.servos[arm][i] != -1:
            config.kit.servo[config.servos[arm][i]].angle = servo_angles[i]


def move(target_position, arm):
    
    angles = solve_ik_3d(target_position, arm)
    servo_angles = translate_angles(angles)
    move_arm(servo_angles, arm)

    print(f"Moved to target: {target_position} | Angles: {angles} | Servo Angles: {servo_angles}")


