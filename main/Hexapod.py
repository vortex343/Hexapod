from Leg import Leg

class Hexabot:
    """
    Represents a hexapod robot with six legs, capable of controlling and managing its movement.

    Attributes:
        legs (Dict[str, Leg]): A dictionary mapping leg names (str) to their corresponding `Leg` objects.

    Methods:
        __init__(self, legs):
            Initializes the Hexabot with a given set of legs.
    """


    def __init__(self, legs: dict[str, Leg]):
        """
        Initializes the Hexabot with a given set of legs.

        Args:
            legs (Dict[str, Leg]): A dictionary mapping leg names (str) to corresponding `Leg` objects.
        """
        self.legs = legs
        