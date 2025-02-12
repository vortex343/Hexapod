import pygame # type: ignore
import time
import init

def main():
    clock = pygame.time.Clock()  
    """initialize the joystick, button mappings, legs and joints"""
    button_mappings, axis_mappings, hat_mappings = init.initialize_button_mapping()
    joystick = init.initialize_joystick()
    hexabot = init.initialize_Hexabot()

    """Main loop"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                Abutton = joystick.get_button(button_mappings['button_A'])
                Bbutton = joystick.get_button(button_mappings['button_B'])

                if Abutton:
                    x = 10
                    y = 10
                    z = float(input('z start: '))
                    z2 = float(input('z goal: '))
                    for i in range(int(z),int(z2)):
                        try:
                            hexabot.legs['back_right'].move_to_relative_fixed_position([-x,y,-i])
                        except:
                            print("Couldn't move leg")
                        try:
                            hexabot.legs['front_right'].move_to_relative_fixed_position([x,y,-i])
                        except:
                            print("Couldn't move leg")
                        try:
                            hexabot.legs['back_left'].move_to_relative_fixed_position([-x,-y,-i])
                        except:
                            print("Couldn't move leg")
                        try:
                            hexabot.legs['front_left'].move_to_relative_fixed_position([x,-y,-i])
                        except:
                            print("Couldn't move leg")
                        try:
                            hexabot.legs['middle_left'].move_to_relative_fixed_position([0,-y,-i])
                        except:
                            print("Couldn't move leg")
                        try:
                            hexabot.legs['middle_right'].move_to_relative_fixed_position([0,y,-i])
                        except:
                            print("Couldn't move leg") 
                        print('done')
                        time.sleep(1)


                if Bbutton:
                    print("Exiting...")
                    exit()
            elif event.type == pygame.JOYAXISMOTION:
                # axis = joystick.get_axis(axis_mappings['axis_name'])
                pass

            elif event.type == pygame.JOYHATMOTION:
                #hat_x, hat_y = joystick.get_hat(hat_mappings['hat_name'])
                pass                    

        # Add a small delay to reduce CPU usage
        clock.tick(60)  

if __name__ == "__main__":
    main()