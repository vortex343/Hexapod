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
        
    async def move_leg_group(self, legs, step, step_height, direction):
        tasks = []
        for leg in legs:
            target = leg.position_relative.copy()
            target[0] += step * direction
            target[2] += step_height
            tasks.append(leg.move_continuous(target, 20))
        await asyncio.gather(*tasks)

    async def move_forward(self):
        group_A = self.legs['front_left'], self.legs['middle_right'], self.legs['back_left']
        group_B = self.legs['front_right'], self.legs['middle_left'], self.legs['back_right']
        sleeptime = 0.1
        step = 5
        step_height = 10

        #Move group a forward
        await self.move_leg_group(group_A, step, step_height, 1)
        await asyncio.sleep(sleeptime)

        await self.move_leg_group(group_A, step, -step_height, 0)
        await asyncio.sleep(sleeptime)

        #Move Body forward
        await self.move_leg_group(group_A + group_B, step, 0, -1)
        await asyncio.sleep(sleeptime)

        #Move group b forward
        await self.move_leg_group(group_B, step, step_height, 1)
        await asyncio.sleep(sleeptime)

        await self.move_leg_group(group_B, step, -step_height, 0)
        await asyncio.sleep(sleeptime)
