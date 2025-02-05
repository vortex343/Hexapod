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

# Print joystick info (name, number of buttons, axes, etc.)
print(f"Joystick name: {joystick.get_name()}")
print(f"Number of buttons: {joystick.get_numbuttons()}")
print(f"Number of axes: {joystick.get_numaxes()}")

# Main loop to test button and axis inputs
try:
    while True:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Detect button presses
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released")

            # Detect axis movements
            elif event.type == pygame.JOYAXISMOTION:
                axis_value = joystick.get_axis(event.axis)
                print(f"Axis {event.axis} moved to {axis_value:.2f}")

        time.sleep(0.1)  # Small delay to prevent too much output

except KeyboardInterrupt:
    pygame.quit()
    print("Test stopped by user.")
