import pygame # type: ignore
import time
import init

def main():
    """initialize the joystick, button mappings, legs and joints"""
    button_mappings, axis_mappings = init.initialize_button_mapping()
    joystick = init.initialize_joystick()
    hexabot = init.initialize_Hexabot()

    """Main loop"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                Abutton = joystick.get_button(button_mappings['button_A'])
                Bbutton = joystick.get_button(button_mappings['button_B'])
                Xbutton = joystick.get_button(button_mappings['button_X'])

                if Abutton:
                    x = 5
                    y = 10
                    z = float(input('z start: '))
                    z2 = float(input('z goal: '))
                    for i in range(int(z),int(z2)):
                        try:
                            hexabot.legs['back_right'].move_to_relative_fixed_position([-x,y,-i])
                            hexabot.legs['front_right'].move_to_relative_fixed_position([x,y,-i])
                            hexabot.legs['back_left'].move_to_relative_fixed_position([-x,-y,-i])
                            hexabot.legs['front_left'].move_to_relative_fixed_position([x,-y,-i])
                            print('done')
                            time.sleep(1)
                        except:
                            print('Could not move right leg to target position')

                if Bbutton:
                    print("Exiting...")
                    exit()                    

        # Add a small delay to reduce CPU usage
        time.sleep(0.05)

if __name__ == "__main__":
    main()