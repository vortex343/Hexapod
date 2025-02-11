import config

class Joint:
    angle: float = 0

    def __init__(self, pin: int, offset: int, inverted: bool):
        self.pin = pin
        self.offset = offset
        self.inverted = inverted
        if 0 <= pin <= 15:
            config.kit.servo[pin].actuation_range = config.actuation_range


    def move(self, angle: float):
        self.angle = angle
        config.kit.servo[self.pin].angle = angle
