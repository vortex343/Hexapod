import math
import time
from Joint import Joint

class Leg:
    _position_global : list[float] = [0,0,0]
    _position_relative : list [float] = [0,0,0]

    def __init__(self, offset : list[float], joints : list[Joint], lengths : list[float]):
        self.offset = offset
        self.joints = joints
        self.lengths = lengths
        return 
    
    def move_to_global_fixed_position(self, target_position : list[float]):        
        global_position_old = self._position_global
        try:
            self.set_position_global(target_position)
            # relative target_position = [x, y, z]
            x = target_position[0] + self.offset[0]
            y = target_position[1] + self.offset[1]
            z = (target_position[2] + self.offset[2])

            target_position = [x, y, z]
            self.move_to_relative_fixed_position(target_position)
            
        except:
            self.set_position_global(global_position_old)
            raise ValueError("Could not move to target position")
    
    def move_to_relative_fixed_position(self, target_position: list[float]):
        relative_position_old = self._position_relative
        try:
            self.set_position_relative(target_position)
            angles = self.solve_ik_3d(target_position)
            self.move(angles)
        except:
            self.set_position_relative(relative_position_old)
            raise ValueError("Could not move to target position")

    def move(self, angles : float):
        for angle, joint in zip(angles, self.joints):
            joint.move(angle)

    def move_with_arc(self, target_position : list[float]):
        steps = self.calc_mvmnt_steps(self._position_relative, target_position, 25)
        for step in steps:
            self.move_to_relative_fixed_position(step)
            time.sleep(0.1)
        
    @staticmethod
    def calc_mvmnt_steps(start : list[float], end : list[float], steps : int):
        steps_list = []
        for i in range(steps + 1):
            t = i / steps
            x = start[0] + t * (end[0] - start[0])
            y = start[1] + t * (end[1] - start[1])
            z = start[2] + t * (end[2] - start[2]) 
            steps_list.append([x, y, z])
        return steps_list

    def solve_ik_3d(self,target_position : list[float]):
        x = target_position[0]
        y = target_position[1]
        z = -target_position[2]

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
