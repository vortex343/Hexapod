import asyncio
from Leg import Leg
import config

class Hexapod:
    """
    Represents a hexapod robot with six legs, capable of controlling and managing its movement.

    Attributes:
        legs (Dict[str, Leg]): A dictionary mapping leg names (str) to their corresponding `Leg` objects.

    Methods:
        __init__(self, legs):
            Initializes the Hexabot with a given set of legs.
    """
    step_x = config.step_x
    step_z = config.step_z


    def __init__(self, legs: dict[str, Leg]):
        """
        Initializes the Hexabot with a given set of legs.

        Args:
            legs (Dict[str, Leg]): A dictionary mapping leg names (str) to corresponding `Leg` objects.
        """
        self.legs = legs

        self.group_fl_mr_bl = self.legs['front_left'], self.legs['middle_right'], self.legs['back_left']
        self.group_fr_ml_br = self.legs['front_right'], self.legs['middle_left'], self.legs['back_right']

        self.group_fl_bl = self.legs['front_left'], self.legs['back_left']
        self.group_fr_br = self.legs['front_right'], self.legs['back_right']
        self.group_mr = tuple([self.legs['middle_right']])
        self.group_ml = tuple([self.legs['middle_left']])
        

#--------------------helper functions--------------------
    async def to_home_position(self):
        """
        Moves all legs to their home position.
        """
        x = 6
        y = 7
        z = -18
        #TODO add home to config and move to_home() to leg
        tasks = []
        tasks.append(self.legs['back_right'].move_continuous([-x,y,z+2], 20))
        tasks.append(self.legs['front_right'].move_continuous([x,y,z], 20))

        tasks.append(self.legs['back_left'].move_continuous([-x,-y,z+2], 20))
        tasks.append(self.legs['front_left'].move_continuous([x,-y,z], 20))
        
        tasks.append(self.legs['middle_right'].move_continuous([0,y,z], 20))
        tasks.append(self.legs['middle_left'].move_continuous([0,-y,z], 20))
        await asyncio.gather(*tasks)

    async def move_leg_group(self, legs, x,y,z):
        """
        Moves a group of legs to a relative position.

        Args:
            legs (List[Leg]): A list of Legs to move.
            x (float): The relative x position to move the legs.
            y (float): The relative y position to move the legs.
            z (float): The relative z position to move the legs.
        """

        tasks = []
        for leg in legs:
            target = leg.position_relative.copy()
            target[0] += x
            target[1] += y
            target[2] += z
            tasks.append(leg.move_continuous(target))
        await asyncio.gather(*tasks)

#--------------------movement functions--------------------
    async def move_start(self, direction = 1):
        """
        Starts the movement of the hexapod in the given direction.
        
        Args:
            direction (int): The direction in which to move the hexapod.
        """

        step_x = self.step_x * direction
        step_z = self.step_z

        await self.to_home_position()

        #Move group a forward
        await self.move_leg_group(self.group_fl_mr_bl, 0, 0, step_z)
        await self.move_leg_group(self.group_fl_mr_bl, step_x, 0, 0)
        await self.move_leg_group(self.group_fl_mr_bl, 0, 0, -step_z)
    
    async def move_during(self, direction = 1):
        """
        Continues the movement of the hexapod in the given direction.
        
        Args:
            direction (int): The direction in which to move the hexapod.
        """
        step_x = self.step_x * direction
        step_z = self.step_z

        #Move Body forward
        await self.move_leg_group(self.legs, -step_x, 0, 0)

        #Move group b forward 2x
        await self.move_leg_group(self.group_fr_ml_br, 0, 0, step_z)
        await self.move_leg_group(self.group_fr_ml_br, step_x * 2, 0, 0)
        await self.move_leg_group(self.group_fr_ml_br, 0, 0, -step_z)

        #Move Body forward
        await self.move_leg_group(self.group_fl_mr_bl + self.group_fr_ml_br, -step_x, 0, 0)

        #Move group a forward 2x
        await self.move_leg_group(self.group_fl_mr_bl, 0, 0, step_z)
        await self.move_leg_group(self.group_fl_mr_bl, step_x * 2, 0, 0)
        await self.move_leg_group(self.group_fl_mr_bl, 0, 0, -step_z)

    async def move_end(self, direction = 1):
        """
        Finishes the movement of the hexapod in the given direction.
        
        Args:
            direction (int): The direction in which to move the hexapod.
        """
        await self.to_home_position()

#--------------------rotation functions--------------------
    async def rotate_start(self, direction):
        """
        Starts the rotation of the hexapod in the given direction.
        
        Args:
            direction (int): The direction in which to move the hexapod.
        """
        await self.to_home_position()

    async def rotate_during(self, direction):
        """
        Continues the rotation of the hexapod in the given direction.
        
        Args:
            direction (int): The direction in which to move the hexapod.
        """
        step_x = self.step_x * direction
        step_z = self.step_z
        self.group_fl_mr_bl = self.legs['front_left'], self.legs['back_left']
        self.group_fr_ml_br = self.legs['front_right'], self.legs['back_right']
        self.group_mr = tuple([self.legs['middle_right']])
        self.group_ml = tuple([self.legs['middle_left']])

        #move group A forward and move group C backward
        await self.move_leg_group(self.group_fl_bl + self.group_mr, 0, 0, step_z)
        tasks = []
        tasks.append(self.move_leg_group(self.group_fl_bl, step_x, 0, 0))
        tasks.append(self.move_leg_group(self.group_mr, -step_x, 0, 0))
        await asyncio.gather(*tasks)
        await self.move_leg_group(self.group_fl_mr_bl, 0, 0, -step_z)

        #move group D forward and move group B backward
        await self.move_leg_group(self.group_fr_br + self.group_ml, 0, 0, step_z)
        tasks = []
        tasks.append(self.move_leg_group(self.group_fr_br, -step_x, 0, 0))
        tasks.append(self.move_leg_group(self.group_ml, step_x, 0, 0))
        await asyncio.gather(*tasks)
        await self.move_leg_group(self.group_fr_ml_br, 0, 0, -step_z)

        #move group A forward and move group C backward
        tasks = []
        tasks.append(self.move_leg_group(self.group_fl_bl, -step_x, 0, 0))
        tasks.append(self.move_leg_group(self.group_mr, step_x, 0, 0))

        #move group D forward and move group B backward
        tasks.append(self.move_leg_group(self.group_fr_br, step_x, 0, 0))
        tasks.append(self.move_leg_group(self.group_ml, -step_x, 0, 0))
        await asyncio.gather(*tasks)

    async def rotate_end(self, direction):
        """
        Finishes the rotation of the hexapod in the given direction.
        
        Args:
            direction (int): The direction in which to move the hexapod.
        """
        await self.to_home_position()
         

