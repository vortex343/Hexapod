from Leg import Leg

class Hexabot:
    def __init__(self, legs: dict[str, Leg]):
        self.legs = legs
        return
        

    def move():
        pass

    def move_leg(self, leg:Leg, target_position : list[float]):        
        global_position_old = leg._position_global
        try:
            leg.set_position_global(target_position)
            # relative target_position = [x, y, z]
            x = target_position[0] + leg.offset[0]
            y = target_position[1] + leg.offset[1]
            z = target_position[2] + leg.offset[2]

            target_position = [x, y, z]
            leg.move_to_relative_fixed_position(target_position)
            
        except:
            leg.set_position_global(global_position_old)
            raise ValueError("Could not move to target position")