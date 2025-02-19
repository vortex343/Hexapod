import time
import pygame 
import init

def main():
    
    #initialize objects and mappings
    clock = pygame.time.Clock()  
    button_mappings, axis_mappings, hat_mappings = init.initialize_controller_mapping()
    controller = init.initialize_joystick()
    hexabot = init.initialize_Hexabot()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                # Press Button 
                # button_name = joystick.get_button(button_mappings['button_name'])

                button_A = controller.get_button(button_mappings['button_A'])
                button_B = controller.get_button(button_mappings['button_B'])
                button_X = controller.get_button(button_mappings['button_X'])
                button_Y = controller.get_button(button_mappings['button_Y'])


                if button_A:
                    x = 10
                    y = 10
                    z1 = int(input('z start: '))
                    z2 = int(input('z goal: '))
                    step = 1
                    diff = 0.5
                    if z1 > z2:
                        step = -step

                    for i in range(z1, z2, step):
                        print(i)
                        z = i*diff
                        try:
                            hexabot.legs['back_right'].move_to_relative_fixed_position([-x,y,z+2])
                            hexabot.legs['front_right'].move_to_relative_fixed_position([x,y,z])

                            hexabot.legs['back_left'].move_to_relative_fixed_position([-x,-y,z+2])
                            hexabot.legs['front_left'].move_to_relative_fixed_position([x,-y,z])

                            
                            x = x - 0.5*diff
                            y = y - 0.5*diff
                            
                            time.sleep(0.1)
                        except:
                            print(f"Stopped at z = {z}!")
                            break

                if button_X:
                    x = float(input('x: '))
                    y = float(input('y: '))
                    z = float(input('z: '))

                    hexabot.legs['back_left'].move_to_relative_fixed_position([x,y,z])
                
                if button_B:
                    print("Exiting...")
                    exit()

            elif event.type == pygame.JOYBUTTONUP:
                # Release Button
                # button_name = joystick.get_button(button_mappings['button_name'])
                pass

            elif event.type == pygame.JOYAXISMOTION:
                # Joystick Position
                # axis = joystick.get_axis(axis_mappings['axis_name'])
                pass

            elif event.type == pygame.JOYHATMOTION:
                # D-Pad
                #hat_x, hat_y = joystick.get_hat(hat_mappings['hat_name'])
                pass                    

        # Frequenzy of Loop
        clock.tick(60)  

if __name__ == "__main__":
    main()