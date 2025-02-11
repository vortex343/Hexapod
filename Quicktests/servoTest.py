from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

# Set up servo on channel 0
servo_channel = int(input("Enter Servo: "))
kit.servo[servo_channel].actuation_range = 125
kit.servo[servo_channel].angle = int(input("Enter angle: "))

