from adafruit_servokit import Servo

class Joint:
    """
    Joint is a part of a leg and represents the servo

    Attributes:
        offset (int): the angle which is set at 0°
        inverted (bool): 
            True means the servo moves in the opposite direction as calculated angle
            False means the servo moves in the same direction as calculated angle
    """

    def __init__(self, offset: int, inverted: bool, actuation_range : int, servo : Servo):
        self.offset = offset
        self.inverted = inverted
        self.actuation_range = actuation_range
        self.servo = servo

        self.servo.actuation_range = actuation_range



    def move(self, angle: float):
        """
        moves the servo of the joint to the given angle

        Args:
            angle (float): the angle which to set the servo

        Raises:
            ValueError: if angle out of range out of range!
        """

        if self.inverted:
            angle = (self.offset - angle) % 360
        else:
            angle = (angle + self.offset) % 360
        if not 0 <= angle <= self.actuation_range:
            raise ValueError(f"Angle {angle} out of range!")
        
        self.servo.angle = angle
