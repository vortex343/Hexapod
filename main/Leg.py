import math
from Joint import Joint
import config

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
            z = target_position[2] + self.offset[2]

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
            if joint.pin < 0:
                continue
            final_angle = angle
            final_angle = (final_angle - joint.offset + 360) % 360
            if joint.inverted == True:
                final_angle = config.actuation_range - final_angle

            if final_angle > config.actuation_range or final_angle < 0:
                print(f"Angle is out of range: {final_angle}, real angle {angle}, for servo {joint.pin}")
                raise ValueError("Angle is out of range")
            
            print(f"Moved servo {joint.pin} to servo angle {final_angle}, real angle {angle}")
            joint.move(final_angle)


    def solve_ik_3d(self, target_position: list[float]):
        x = target_position[0]
        y = target_position[1] 
        z = target_position[2]  # Adjusting for coordinate system

        # Leg segment lengths
        l1 = self.lengths[0]  # Hip segment length (if applicable)
        l2 = self.lengths[1]  # Thigh length
        l3 = self.lengths[2]  # Shin length

        # Compute horizontal plane distance
        d = math.sqrt(x**2 + y**2)  # XY plane projection
        c = math.sqrt(d**2 + z**2)  # Total 3D distance

        # Hip yaw rotation (rotation around vertical axis)
        angle1 = math.atan2(x, y)

        # Law of Cosines to compute knee angle
        angle3 = math.acos((l2**2 + l3**2 - c**2) / (2 * l2 * l3))

        # Compute angle for thigh using Law of Cosines
        temp1 = math.acos((l2**2 + c**2 - l3**2) / (2 * l2 * c))
        temp2 = math.atan2(z, d)  # Adjusted projection
        angle2 = temp2 + temp1  # Adjusting thigh angle

        return [math.degrees(angle1), math.degrees(angle2), math.degrees(angle3)]

    def set_position_relative(self, pos : list[float]):
        self._position_relative = pos
    
    def set_position_global(self, pos : list[float]):
        self._position_global = pos

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
