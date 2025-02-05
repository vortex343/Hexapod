from adafruit_servokit import ServoKit
import time
import pygame

#init controller
pygame.init()
pygame.joystick.init()

# Check if any joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected!")
    exit()


# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()



#kit.servo[0].angle = 180               for angle
#kit.continuous_servo[1].throttle = 1   for continuous throttle

# Initialize the ServoKit for a 16-channel Servo Hat
kit = ServoKit(channels=16)

# Set up servo on channel 0
servo_channel = 0

def map_axis_to_angle(value):
    return int((value + 1) * 90)  # Maps -1 to 1 -> 0 to 180



while True:
    for event in pygame.event.get():
        # Skip irrelevant events
        if event.type not in [pygame.JOYAXISMOTION]:
            continue

        # Get the joystick axis values
        x_value = joystick.get_axis(0)  # Left stick X-axis
        y_value = joystick.get_axis(1)  # Left stick Y-axis

        # Map axis values to servo angles
        x_angle = map_axis_to_angle(x_value)
        y_angle = map_axis_to_angle(y_value)

        # Update servos with mapped angles
        kit.servo[0].angle = x_angle  # Servo on Channel 0
        kit.servo[1].angle = y_angle  # Servo on Channel 1

        # Print the angles for debugging
        print(f"X-axis angle: {x_angle}, Y-axis angle: {y_angle}")

    # Add a small delay to reduce CPU usage
    time.sleep(0.05)