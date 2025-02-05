import config

class Joint:
    def __init__(self, pin, offset):
        servo = config.kit.servo[pin]
        servo.actuation_range = config.actuation_range
        self.offset = offset
    

    def move(self, angle):
        final_angle = (angle + self.offset + 360) % 360
        if final_angle > config.actuation_range:
            raise ValueError("Angle is out of range")

        self.servo.angle = final_angle