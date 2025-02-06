import config

class Joint:
    angle: float = 0

    def __init__(self, pin: int, offset: int):
        self.pin = pin
        config.kit.servo[pin].actuation_range = config.actuation_range
        self.offset = offset

    def move(self, angle: float):
        final_angle = (angle - self.offset + 360) % 360
        if final_angle > config.actuation_range:
            print(f"Angle is out of range: {final_angle} for servo {self.pin}")
            raise ValueError("Angle is out of range")
        self.angle = final_angle
        config.kit.servo[self.pin].angle = final_angle
