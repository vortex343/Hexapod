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
                    try:
                        # Example target position (in cm)
                        x = float(input('x: '))
                        y = float(input('y: '))
                        z = float(input('z: '))
                        target_position = [x,y,z]  # Target (x, y, z)
                        hexabot.legs['front_right'].move_to_relative_fixed_position(target_position)
                        print('done')
                    except:
                        print('Could not move to target position')

                if Bbutton:
                    print("Exiting...")
                    exit()                    

        # Add a small delay to reduce CPU usage
        time.sleep(0.05)

if __name__ == "__main__":
    main()