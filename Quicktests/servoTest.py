from adafruit_servokit import ServoKit  # type: ignore
import time

#kit.servo[0].angle = 180               for angle
#kit.continuous_servo[1].throttle = 1   for continuous throttle

# Initialize the ServoKit for a 16-channel Servo Hat
kit = ServoKit(channels=16)



# Set up servo on channel 0
servo_channel = 0

kit.servo[servo_channel].actuation_range = 125


kit.servo[servo_channel].angle = 0
print(0)

