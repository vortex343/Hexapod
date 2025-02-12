import pygame
import time

# Initialize Pygame and the joystick module
pygame.init()
pygame.joystick.init()

# Check if any joystick is connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected!")
    exit()

# Get the first joystick (controller)
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Print joystick info
print(f"Joystick name: {joystick.get_name()}")
print(f"Number of buttons: {joystick.get_numbuttons()}")
print(f"Number of axes: {joystick.get_numaxes()}")
print(f"Number of hats (D-pad): {joystick.get_numhats()}")  # Check for D-pad

# Main loop to test inputs
try:
    while True:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Detect button presses
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released")

            # Detect axis movements
            elif event.type == pygame.JOYAXISMOTION:
                axis_value = joystick.get_axis(event.axis)
                print(f"Axis {event.axis} moved to {axis_value:.2f}")

            # Detect D-pad (hat) movement
            elif event.type == pygame.JOYHATMOTION:
                hat_x, hat_y = joystick.get_hat(0)
                print(f"D-pad moved: ({hat_x}, {hat_y})")

        time.sleep(0.1)  # Small delay to prevent too much output

except KeyboardInterrupt:
    pygame.quit()
    print("Test stopped by user.")
