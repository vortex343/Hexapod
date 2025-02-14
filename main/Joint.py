from adafruit_servokit import Servo

class Joint:
    """
    Joint is a part of a leg and represents the servo

    Attributes:
        offset (int): the angle which is set at 0°
        inverted (bool): 
            True means the servo moves clockwise
            False means the servo moves counter-clockwise
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

        angle = (angle + self.offset) % 360
        if not 0 <= angle <= self.actuation_range:
            raise ValueError("Angle out of range!")
        
        if self.inverted:
            angle = self.actuation_range - angle

        self.servo = angle
