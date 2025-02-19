from adafruit_servokit import ServoKit  # type: ignore
import time

kit = ServoKit(channels=16)
input = int(input("Enter: "))
for i in range(16):
    kit.servo[i].actuation_range = 135
    kit.servo[i].angle = input
