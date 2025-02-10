import config

class Joint:
    angle: float = 0

    def __init__(self, pin: int, offset: int, inverted: bool):
        if 0 <= pin <= 15:
            self.pin = pin
            config.kit.servo[pin].actuation_range = config.actuation_range
            self.offset = offset
            self.inverted = inverted

    def move(self, angle: float):
        self.angle = angle
        config.kit.servo[self.pin].angle = angle
