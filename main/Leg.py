import math
import config
import Joint

class Leg:
    lenghts = config.lenghts
    _position_global : list[float] = [0,0,0]
    _position_relative : list [float] = [0,0,0]

    def __init__(self, offset : list[float], joints : list[Joint.Joint], lengths : list[float]):
        self.offset = offset
        self.joints = joints
        self.lengths = lengths
        return 
    
    def move_to_global_fixed_position(self, target_position : list[float]):        
        # relative target_position = [x, y, z]
        x = target_position[0] + self.offset
        y = target_position[1] + self.offset
        z = -(target_position[2] + self.offset)

        target_position = [x, y, z]
        
        self.move_to_relative_fixed_position(target_position)


    def move_to_relative_fixed_position(self, target_position : list[float]):
        angles = self.solve_ik_3d(target_position)
        self.move(angles)

    def move(self, angles : float):
        for angle, joint in zip(angles, self.joints):
            joint.move(angle)
        	

    def solve_ik_3d(self,target_position : list[float]):
        x = target_position[0]
        y = target_position[1]
        z = target_position[2]

        # leg dimensions
        l2 = self.lengths[1]
        l3 = self.lengths[2]
        
        c = math.sqrt(x**2 + y**2)

        # Calculate angles
        angle1 = math.atan2(x, y)

        angle3 = math.acos((l2**2 + l3**2 - c**2) / (2 * l2 * l3))

        temp1 = math.acos((l2**2 + c**2 - l3**2) / (2 * l2 * c))
        temp2 = math.atan2(z , y)
        angle2 = temp1 - temp2

        return [math.degrees(angle1), math.degrees(angle2), math.degrees(angle3)]

    def set_position_relative(self, pos : list[float]):
        self._position_relative = pos
    
    def set_position_global(self, pos : list[float]):
        self._position_global = pos
