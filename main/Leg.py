import math
import config
from Joint import Joint
import asyncio

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
        self.position_relative = [0, 0, 0]  

    
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

    async def move_continuous(self, target_position: list[float], steps: int = config.step_count, delay: float = config.delay):
        """
        Moves the Leg to a target position in a continuous manner by breaking the movement into smaller steps.

        Args:
            target_position (list[float]): The target position in relative coordinates [x, y, z].
            steps (int): The number of steps to break the movement into.
            delay (float): The delay between each step in seconds.
        """
        pos = self.position_relative.copy()  # Copy to avoid modifying original
        step_size = [(target_position[i] - pos[i]) / steps for i in range(3)]  # Compute incremental step

        for _ in range(steps):  # Ensure smooth motion
            pos = [pos[i] + step_size[i] for i in range(3)]  # Update each coordinate incrementally
            self.move_to_relative_fixed_position(pos)
            await asyncio.sleep(delay)


    def solve_ik_3d(self, target_position: list[float]):
        """
        Solves the inverse kinematics for a 3D position.

        Args:
            target_position (list[float]): The target position in 3D space [x, y, z].

        Returns:
            list[float]: A list of angles [angle1, angle2, angle3] for the joints.
        """

        x, y, z = target_position
        l1,l2, l3 = self.lengths

        d = math.sqrt(x**2 + y**2)  
        c = math.sqrt(d**2 + z**2)  

        angle1 = math.atan2(x, y)

        temp1 = math.acos((l2**2 + c**2 - l3**2) / (2 * l2 * c))
        temp2 = math.atan2(z, d)  
        angle2 = temp2 + temp1  

        angle3 = math.acos((l2**2 + l3**2 - c**2) / (2 * l2 * l3))

        return math.degrees(angle1), math.degrees(angle2), math.degrees(angle3)


class Leg2Joints(Leg):
        """
        Leg2Joints extends Leg is a Leg with only 2 Joints and therfore has not the full rang of motion in 3d space.
        The class overrides the move_to_relative_fixed_position() method to move the leg in 2D space.

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
            self.joints = [joints[0],joints[1]]
            self.lengths = lengths
            self.position_relative = [0, 0, 0] 
            return
        
        def move_to_relative_fixed_position(self, target_position: list[float]):
            """
            Moves the 2-joint leg to a relative position by computing the correct x (forward) 
            using hip rotation and the correct z (height) using knee rotation.
            """
            x, y, z = target_position
            l1, l2 = self.lengths  # l1 = hip to knee, l2 = knee to foot

            # Hip rotation should determine the forward x position
            hip_rotation = math.degrees(math.asin(x/l2))

            # Knee rotation should determine the height z
            knee_rotation = math.degrees(math.asin(z/l2))  

            # Move the joints
            self.joints[0].move(hip_rotation)  # Move hip
            self.joints[1].move(knee_rotation)  # Move knee

            self.position_relative = target_position
