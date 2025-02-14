import math
from Joint import Joint

class Leg:
    """
    Leg is a part of the Hexapod and represents a 3 Joint Leg.
    The class contains methods for movement and solving inverse Kinematics

    Attributes:
        offset (list[float]): The offset position of the leg in the global space.
        joints (list[Joint]): A list of Joint objects representing the leg's joints.
        lengths (list[float]): The lengths of the leg segments (e.g., hip, thigh, shin).
        position_relative (list[float]): The current relative position of the leg.
    """


    def __init__(self, offset : list[float], joints : list[Joint], lengths : list[float]):
        """
        Initializes the leg with the provided offset, joints, and segment lengths.

        Args:
            offset (list[float]): The offset position of the leg in the global space.
            joints (list[Joint]): A list of Joint objects representing the leg's joints.
            lengths (list[float]): The lengths of the leg segments (e.g., hip, thigh, shin).
        """

        self.offset = offset
        self.joints = joints
        self.lengths = lengths
        position_relative = [0,0,0]
        return 
    
    
    def move_to_global_fixed_position(self, target_position : list[float]):
        """
        Moves the Leg to a global target position by adding the offsets and calling move_to_relative_fixed_position()

        Args:
            target_position (list[float]): The target position in global coordinates [x, y, z].
        """

        x = target_position[0] + self.offset[0]
        y = target_position[1] + self.offset[1]
        z = target_position[2] + self.offset[2]

        self.move_to_relative_fixed_position([x, y, z])

    
    def move_to_relative_fixed_position(self, target_position: list[float]):
        """
        Moves the Leg to a relative target position, by calculating the inverse kinematics

        Args:
            target_position (list[float]): The target position in relative coordinates [x, y, z].
        """

        angles = self.solve_ik_3d(target_position)
        for angle, joint in zip(angles, self.joints):
            joint.move(angle)
        self.position_relative = target_position


    def solve_ik_3d(self, target_position: list[float]):
        """
        Solves the inverse kinematics for a 3D position.

        Args:
            target_position (list[float]): The target position in 3D space [x, y, z].

        Returns:
            list[float]: A list of angles [angle1, angle2, angle3] for the joints.
        """

        x, y, z = target_position
        l2, l3 = self.lengths

        d = math.sqrt(x**2 + y**2)  
        c = math.sqrt(d**2 + z**2)  

        angle1 = math.atan2(x, y)

        temp1 = math.acos((l2**2 + c**2 - l3**2) / (2 * l2 * c))
        temp2 = math.atan2(z, d)  
        angle2 = temp2 + temp1  

        angle3 = math.acos((l2**2 + l3**2 - c**2) / (2 * l2 * l3))

        return math.degrees(angle1), math.degrees(angle2), math.degrees(angle3)


class Leg2Joints(Leg):
        def __init__(self, offset : list[float], joints : list[Joint], lengths : list[float]):
            self.offset = offset
            self.joints = [joints[0],joints[1]]
            self.lengths = lengths
            return
        
        def move_to_relative_fixed_position(self, target_position: list[float]):
            x = target_position[0]
            y = target_position[1] 
            z = target_position[2]  

            height = math.degrees(math.atan(z/y))
            rotation = math.degrees(math.atan(x/y))
            
            self.move([rotation, height])
