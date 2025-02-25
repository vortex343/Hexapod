import traceback
import pygame
import init
import asyncio
import os
import sys
import cv2
from flask import Flask, Response
import threading 
from threading import Thread, Event
from werkzeug.serving import make_server

# Flask app setup
app = Flask(__name__)

# Global control flags
stop_event = Event()
camera_running = Event()

# Global threads
cam_thread = None
server = None
main_thread = None



def main():
    global cam_thread
    
    clock = pygame.time.Clock()
    button_mappings, axis_mappings, hat_mappings = init.initialize_controller_mapping()
    controller = init.initialize_joystick()
    global hexapod 
    hexapod = init.initialize_Hexapod()
    
    dpad_y_pressed, dpad_x_pressed = False, False
    asyncio.run(hexapod.speaker_beep(0.25, 261))
    asyncio.run(hexapod.speaker_beep(0.25, 329))
    asyncio.run(hexapod.speaker_beep(0.25, 392))
    asyncio.run(hexapod.speaker_beep(0.25, 523))

    try:
        while not stop_event.is_set():
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    button_X = controller.get_button(button_mappings['button_X'])
                    button_Y = controller.get_button(button_mappings['button_Y'])
                    select = controller.get_button(button_mappings['button_select'])
                    start = controller.get_button(button_mappings['button_start'])
                    button_stick_L = controller.get_button(button_mappings['button_LJ'])
                    button_stick_R = controller.get_button(button_mappings['button_RJ'])
                    
                    if button_X:
                        asyncio.run(hexapod.to_home_position())

                    if button_Y:
                        asyncio.run(hexapod.speaker_beep(0.5))
                    
                    if button_stick_L and button_stick_R:
                        print("Exiting...")
                        raise KeyboardInterrupt
                    
                    if select:
                        print("Restarting script...")
                        raise Exception("Restarting script...")
                    
                    if start and not camera_running.is_set():
                        print("Starting camera...")
                        camera_running.set()
                        cam_thread = Thread(target=cam)
                        cam_thread.start()
                
                elif event.type == pygame.JOYHATMOTION:
                    hat_x, hat_y = controller.get_hat(hat_mappings['dpad'])
                    
                    if hat_y != 0 and not dpad_y_pressed:
                        dpad_y_pressed = True
                        asyncio.run(hexapod.move_start(hat_y))
                    elif hat_y == 0 and dpad_y_pressed:
                        dpad_y_pressed = False
                        asyncio.run(hexapod.move_end(hat_y))
                    
                    if hat_x != 0 and not dpad_x_pressed:
                        dpad_x_pressed = True
                        asyncio.run(hexapod.rotate_start(hat_x))
                    elif hat_x == 0 and dpad_x_pressed:
                        dpad_x_pressed = False
                        asyncio.run(hexapod.rotate_end(hat_x))
            
            if dpad_y_pressed:
                asyncio.run(hexapod.move_during(controller.get_hat(hat_mappings['dpad'])[1]))
            if dpad_x_pressed:
                asyncio.run(hexapod.rotate_during(controller.get_hat(hat_mappings['dpad'])[0]))
            
            clock.tick(30)

    except KeyboardInterrupt:
        asyncio.run(shutdown_procedure())
    except Exception as e:
        print(f"Exception in main(): {e}")
        traceback.print_exc()
        asyncio.run(restart_script())

# --------------------------------------Shutdown and restart functions--------------------------------------
async def shutdown_procedure():
    """Handles script shutdown procedures."""
    print("Interrupted by user, shutting down...")

    await (hexapod.speaker_beep(0.25, 523))
    await (hexapod.speaker_beep(0.25, 392))
    await (hexapod.speaker_beep(0.25, 329))
    await (hexapod.speaker_beep(0.25, 261))

    stop_event.set()
    camera_running.set()
    traceback.print_exc()
    
    if main_thread and main_thread.is_alive() and main_thread != threading.current_thread():
        main_thread.join(timeout=5)
    if cam_thread and cam_thread.is_alive():
        cam_thread.join(timeout=5)


async def restart_script():
    """Restarts the script safely."""
    print("Restarting script...")
    await hexapod.speaker_beep(0.25)
    await asyncio.sleep(0.25)
    await hexapod.speaker_beep(0.25)

    stop_event.set()
    camera_running.set()
    
    if server:
        try:
            server.shutdown()
        except Exception as e:
            print(f"Error shutting down Flask server: {e}")
    
    if cam_thread and cam_thread.is_alive():
        cam_thread.join(timeout=5)
    
    print("Restarting now...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

# --------------------------------------Camera server functions--------------------------------------
def cam():
    """Starts the camera server."""
    global server
    
    camera = init.initialize_camera()
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()

def generate_frames():
    """Generates video frames for the Flask video feed."""
    while not stop_event.is_set():
        clock = pygame.time.Clock()
        clock.tick(30)
        frame = cv2.flip(init.initialize_camera().capture_array(), -1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.jpg', frame_rgb)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Flask route for video streaming."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    main_thread = Thread(target=main)
    main_thread.start()
    main_thread.join()
    
    if camera_running.is_set() and cam_thread and cam_thread.is_alive():
        cam_thread.join()
