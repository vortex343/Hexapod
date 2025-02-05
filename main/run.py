import pygame
import time
import Leg
import config
import init

def main():
    """initialize the joystick, button mappings, legs and joints"""
    button_mappings, axis_mappings = init.initialize_button_mapping()
    joystick = init.initialize_joystick()

    """Main loop"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                Abutton = joystick.get_button(button_mappings['button_A'])
                Bbutton = joystick.get_button(button_mappings['button_B'])

                if Abutton:
                    # Example target position (in cm)
                    x =  int(input('x: '))
                    y =  int(input('y: '))
                    z = int(input('z: '))
                    target_position = [x,y,z]  # Target (x, y, z)
                    
                    print('done')

                if Bbutton:
                    print("Exiting...")
                    exit()

        # Add a small delay to reduce CPU usage
        time.sleep(0.05)

if __name__ == "__main__":
    main()