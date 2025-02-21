import time
import pygame 
import init
import asyncio

async def main():
    
    #initialize objects and mappings
    clock = pygame.time.Clock()  
    button_mappings, axis_mappings, hat_mappings = init.initialize_controller_mapping()
    controller = init.initialize_joystick()
    hexapod = init.initialize_Hexapod()


    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                # Press Button 
                # button_name = controller.get_button(button_mappings['button_name'])

                button_A = controller.get_button(button_mappings['button_A'])
                button_B = controller.get_button(button_mappings['button_B'])
                button_X = controller.get_button(button_mappings['button_X'])
                button_Y = controller.get_button(button_mappings['button_Y'])


                if button_A:
                    x = 5
                    y = 15
                    z1 = 0
                    z2 = -40
                    step = 1
                    diff = 0.5
                    if z1 > z2:
                        step = -step

                    for i in range(z1, z2, step):
                        z = i*diff
                        try:
                            hexapod.legs['back_right'].move_to_relative_fixed_position([-x,y,z+2])
                            hexapod.legs['front_right'].move_to_relative_fixed_position([x,y,z])

                            hexapod.legs['back_left'].move_to_relative_fixed_position([-x,-y,z+2])
                            hexapod.legs['front_left'].move_to_relative_fixed_position([x,-y,z])
            

                            y = y - 0.5*diff
                            
                            time.sleep(0.1)
                        except:
                            print(f"error at z = {z} !")
                        try:
                            hexapod.legs['middle_right'].move_to_relative_fixed_position([0,y,z])
                            hexapod.legs['middle_left'].move_to_relative_fixed_position([0,-y,z])
                        except: 
                            print(f"error in the middle at z = {z} !")    

                if button_X:
                    x = 5
                    y = 15
                    z = 0
                    hexapod.legs['back_right'].move_to_relative_fixed_position([-x,y,z+2])
                    hexapod.legs['front_right'].move_to_relative_fixed_position([x,y,z])

                    hexapod.legs['back_left'].move_to_relative_fixed_position([-x,-y,z+2])
                    hexapod.legs['front_left'].move_to_relative_fixed_position([x,-y,z])
                    
                    hexapod.legs['middle_right'].move_to_relative_fixed_position([0,y,z])
                    hexapod.legs['middle_left'].move_to_relative_fixed_position([0,-y,z])
                
                if button_Y:
                    x = int(input("x: "))
                    y = int(input("y: "))
                    z = int(input("z: "))
                    await hexapod.legs['middle_left'].move_continuous([x,y,z], 20)


                if button_B:
                    print("Exiting...")
                    exit()

            elif event.type == pygame.JOYBUTTONUP:
                # Release Button
                # button_name = controller.get_button(button_mappings['button_name'])
                pass

            elif event.type == pygame.JOYAXISMOTION:
                # Joystick Position
                # axis = controller.get_axis(axis_mappings['axis_name'])
                pass

            elif event.type == pygame.JOYHATMOTION:
                # D-Pad
                hat_x, hat_y = controller.get_hat(hat_mappings['dpad'])
                if hat_y == 1:
                    await hexapod.move_forward()
                                    

        # Frequenzy of Loop
        clock.tick(60)  

if __name__ == "__main__":
    asyncio.run(main())