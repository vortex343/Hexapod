import traceback
import pygame 
import init
import asyncio
import os
import sys
from flask import Flask, Response
import cv2
from threading import Thread

app = Flask(__name__)

def main():
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
                    asyncio.run(hexapod.to_home_position())

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
                    asyncio.run(hexapod.move_start(hat_y))
                elif hat_y == 0 and dpad_y_pressed:
                    dpad_y_pressed = False
                    asyncio.run(hexapod.move_end(hat_y))

                #X-Axis
                if hat_x != 0 and not dpad_x_pressed:
                    dpad_x_pressed = True
                    asyncio.run(hexapod.rotate_start(hat_x))
                elif hat_x == 0 and dpad_x_pressed:
                    dpad_x_pressed = False
                    asyncio.run(hexapod.rotate_end(hat_x))

        if dpad_y_pressed:
            asyncio.run(hexapod.move_during(hat_y))
        if dpad_x_pressed:
            asyncio.run(hexapod.rotate_during(hat_x))

        clock.tick(30)

def cam():
    global camera

    camera = init.initialize_camera()

    def run_flask():
        app.run(host='0.0.0.0', port=5000)

    flask_thread = Thread(target=run_flask)
    flask_thread.start()

def generate_frames():
    while True:
        clock = pygame.time.Clock()  
        clock.tick(30)
        # Capture the frame from the camera
        frame = camera.capture_array()
        # Explicitly convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame_rgb)
        frame = buffer.tobytes()

        # Yield the frame as part of an MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    main_thread = Thread(target=main)
    cam_thread = Thread(target=cam)
    
    main_thread.start()
    cam_thread.start()
    
    main_thread.join()
    cam_thread.join()

