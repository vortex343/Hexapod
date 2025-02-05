import pygame
import time
import movement
import config

def main():
    joystick = config.initialize_joystick()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                Abutton = joystick.get_button(config.button_mappings['button_A'])
                Bbutton = joystick.get_button(config.button_mappings['button_B'])

                if Abutton:
                    x =  int(input('x: '))
                    y =  int(input('y: '))
                    z = int(input('z: '))

                    target_position = [x,y,z]
                    movement.move(target_position, 'back_right')
                    print('done')

                if Bbutton:
                    print("Exiting...")
                    exit()

        # Add a small delay to reduce CPU usage
        time.sleep(0.05)

if __name__ == "__main__":
    main()