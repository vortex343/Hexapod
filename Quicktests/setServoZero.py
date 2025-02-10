from adafruit_servokit import ServoKit  # type: ignore
import time

kit = ServoKit(channels=16)
for servo in kit.servo:
    servo.actuation_range = 125
    servo.angle = 0
