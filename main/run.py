import time
import traceback
import pygame 
import init
import asyncio
import os
import sys


async def main():
    
    #initialize objects and mappings
    clock = pygame.time.Clock()  
    button_mappings, axis_mappings, hat_mappings = init.initialize_controller_mapping()
    controller = init.initialize_joystick()
    hexapod = init.initialize_Hexapod()

    dpad_y_pressed = False
    dpad_x_pressed = False

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
                select = controller.get_button(button_mappings['button_select'])
                button_stick_R = controller.get_button(button_mappings['button_RJ'])
                button_stick_L = controller.get_button(button_mappings['button_LJ'])                

                if button_X:
                    await hexapod.to_home_position()

                if button_A:
                    x = 5
                    y = 15
                    z = 0
                    hexapod.legs['back_right'].move_to_relative_fixed_position([-x,y,z+2])
                    hexapod.legs['front_right'].move_to_relative_fixed_position([x,y,z])

                    hexapod.legs['back_left'].move_to_relative_fixed_position([-x,-y,z+2])
                    hexapod.legs['front_left'].move_to_relative_fixed_position([x,-y,z])
                    
                    hexapod.legs['middle_right'].move_to_relative_fixed_position([0,y,z])
                    hexapod.legs['middle_left'].move_to_relative_fixed_position([0,-y,z])
                
                if button_stick_L and button_stick_R:
                    print("Exiting...")
                    exit()

                if select:
                    print("Restarting script...")
                    os.execv(sys.executable, ['python'] + sys.argv)

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

                #Y-Axis
                if hat_y != 0 and not dpad_y_pressed:
                    dpad_y_pressed = True
                    await hexapod.move_start(hat_y)
                elif hat_y == 0 and dpad_y_pressed:
                    dpad_y_pressed = False
                    await hexapod.move_end(hat_y)

                #X-Axis
                if hat_x != 0 and not dpad_x_pressed:
                    dpad_x_pressed = True
                    await hexapod.rotate_start(hat_x)
                elif hat_x == 0 and dpad_x_pressed:
                    dpad_x_pressed = False
                    await hexapod.rotate_end(hat_x)

        if dpad_y_pressed:
            await hexapod.move_during(hat_y)
        if dpad_x_pressed:
            await hexapod.rotate_during(hat_x)

        # Frequenzy of Loop
        clock.tick(60)  

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e: 
        traceback.print_exc()
        print(e)        
        os.execv(sys.executable, ['python'] + sys.argv)
