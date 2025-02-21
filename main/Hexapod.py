import asyncio
import time
from Leg import Leg

class Hexapod:
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
        self.step = 5
        self.step_height = 10
        self.step_count = 20
        self.delay = 0.025

#--------------------helper functions--------------------
    async def to_home_position(self):
        """
        Moves all legs to their home position.
        """
        x = 6
        y = 10
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
        tasks = []
        for leg in legs:
            target = leg.position_relative.copy()
            target[0] += x
            target[1] += y
            target[2] += z
            tasks.append(leg.move_continuous(target, self.step_count, self.delay))
        await asyncio.gather(*tasks)

#--------------------movement functions--------------------
    async def move_start(self, direction):
        step = self.step * direction
        group_A = self.legs['front_left'], self.legs['middle_right'], self.legs['back_left']
        group_B = self.legs['front_right'], self.legs['middle_left'], self.legs['back_right']

        await self.to_home_position()

        #Move group a forward
        await self.move_leg_group(group_A, 0, 0, self.step_height)
        await self.move_leg_group(group_A, step, 0, 0)
        await self.move_leg_group(group_A, 0, 0, -self.step_height)
    
    async def move_during(self, direction):
        step = self.step * direction
        group_A = self.legs['front_left'], self.legs['middle_right'], self.legs['back_left']
        group_B = self.legs['front_right'], self.legs['middle_left'], self.legs['back_right']

        #Move Body forward
        await self.move_leg_group(group_A + group_B, -step, 0, 0)

        #Move group b forward 2x
        await self.move_leg_group(group_B, 0, 0, self.step_height)
        await self.move_leg_group(group_B, step * 2, 0, 0)
        await self.move_leg_group(group_B, 0, 0, -self.step_height)

        #Move Body forward
        await self.move_leg_group(group_A + group_B, -step, 0, 0)

        #Move group a forward 2x
        await self.move_leg_group(group_A, 0, 0, self.step_height)
        await self.move_leg_group(group_A, step * 2, 0, 0)
        await self.move_leg_group(group_A, 0, 0, -self.step_height)

    async def move_end(self, direction):
        await self.to_home_position()

#--------------------rotation functions--------------------
    async def rotate_start(self, direction):
        await self.to_home_position()

    async def rotate_during(self, direction):
        step = self.step * direction
        group_A = self.legs['front_left'], self.legs['back_left']
        group_B = self.legs['front_right'], self.legs['back_right']
        group_C = tuple([self.legs['middle_right']])
        group_D = tuple([self.legs['middle_left']])

        #move group A forward and move group C backward
        await self.move_leg_group(group_A + group_C, 0, 0, self.step_height)
        tasks = []
        tasks.append(self.move_leg_group(group_A, step, 0, 0))
        tasks.append(self.move_leg_group(group_C, -step, 0, 0))
        await asyncio.gather(*tasks)
        await self.move_leg_group(group_A + group_C, 0, 0, -self.step_height)

        #move group D forward and move group B backward
        await self.move_leg_group(group_B + group_D, 0, 0, self.step_height)
        tasks = []
        tasks.append(self.move_leg_group(group_B, -step, 0, 0))
        tasks.append(self.move_leg_group(group_D, step, 0, 0))
        await asyncio.gather(*tasks)
        await self.move_leg_group(group_B + group_D, 0, 0, -self.step_height)

        #move group A forward and move group C backward
        tasks = []
        await self.move_leg_group(group_A, -step, 0, 0)
        await self.move_leg_group(group_C, step, 0, 0)

        #move group D forward and move group B backward
        tasks.append(self.move_leg_group(group_B, step, 0, 0))
        tasks.append(self.move_leg_group(group_D, -step, 0, 0))
        await asyncio.gather(*tasks)

    async def rotate_end(self, direction):
        await self.to_home_position()
         

