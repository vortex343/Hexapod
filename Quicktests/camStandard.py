from picamera2 import Picamera2 # type: ignore
from flask import Flask, Response
import cv2

# Initialize Flask app
app = Flask(__name__)

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1920, 1080)}))
picam2.start()


# Function to generate frames
def generate_frames():
    while True:
        # Capture the frame from the camera
        frame = picam2.capture_array()
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


# Run the web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)