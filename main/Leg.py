import math
import config

class Leg:
    lenghts = config.lenghts
    def __init__(self, position, joints, lengths):
        self.position = position
        self.joints = joints
        self.lengths = lengths
        return 
    
    def move(self, target_position):
        angles = self.solve_ik_3d(target_position)
        
        for angle, joint in zip(angles, self.joints):
            joint.move(angle)
        	

    def solve_ik_3d(self,target_position):

        # relative target_position = [x, y, z]
        x = target_position[0] + self.position
        y = target_position[1] + self.position
        z = -(target_position[2] + self.position)

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

