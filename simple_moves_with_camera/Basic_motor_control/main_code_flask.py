from flask import Flask, render_template, Response
import Jetson.GPIO as GPIO
import cv2

app = Flask(__name__)

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)  # Use BOARD mode
GPIO.setwarnings(False)

# Define motor pins (adjust based on MX1005 setup)
MOTOR_A_FORWARD = 31
MOTOR_A_BACKWARD = 33
MOTOR_B_FORWARD = 35
MOTOR_B_BACKWARD = 37

# Set up motor pins as outputs
GPIO.setup(MOTOR_A_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_A_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_B_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_B_BACKWARD, GPIO.OUT)

# Camera setup using GStreamer pipeline for Jetson Nano
def gstreamer_pipeline(
    capture_width=640,
    capture_height=480,
    display_width=640,
    display_height=480,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

# Motor control functions change for urself
def forward():
    GPIO.output(MOTOR_A_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_A_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_B_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_B_BACKWARD, GPIO.HIGH)

def backward():
    GPIO.output(MOTOR_A_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_A_BACKWARD, GPIO.HIGH)
    GPIO.output(MOTOR_B_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_B_BACKWARD, GPIO.LOW)

def left():
    GPIO.output(MOTOR_A_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_A_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_B_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_B_BACKWARD, GPIO.LOW)

def right():
    GPIO.output(MOTOR_A_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_A_BACKWARD, GPIO.HIGH)
    GPIO.output(MOTOR_B_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_B_BACKWARD, GPIO.HIGH)

def stop():
    GPIO.output(MOTOR_A_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_A_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_B_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_B_BACKWARD, GPIO.LOW)

# Video stream generator
def gen_frames():
    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Error: Unable to open the camera")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break

        # Encode the frame as JPEG for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Error: Failed to encode frame")
            break
        frame = buffer.tobytes()

        # Stream the frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control/<direction>')
def control(direction):
    if direction == 'forward':
        forward()
    elif direction == 'backward':
        backward()
    elif direction == 'left':
        left()
    elif direction == 'right':
        right()
    elif direction == 'stop':
        stop()
    return '', 204

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
    except KeyboardInterrupt:
        GPIO.cleanup()
        cv2.destroyAllWindows()

