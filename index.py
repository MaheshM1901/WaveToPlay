from flask import Flask, render_template, Response, redirect
import cv2
import time
from cvzone.HandTrackingModule import HandDetector

app = Flask(__name__, template_folder='templates')

detector = HandDetector(maxHands=1, detectionCon=0.8)
cam = cv2.VideoCapture(0)

output = ""
last_trigger_time = 0
cooldown_seconds = 3  # Prevents triggering multiple times rapidly

# Gesture mapping
gestures = {
    (0, 0, 0, 0, 0): "10",
    (0, 1, 0, 0, 0): "1",
    (0, 1, 1, 0, 0): "2",
    (0, 1, 1, 1, 0): "3",
    (0, 1, 1, 1, 1): "4",
    (1, 1, 1, 1, 1): "5",
    (1, 0, 0, 0, 0): "6",
    (1, 1, 0, 0, 0): "7",
    (1, 1, 1, 0, 0): "8",
    (1, 1, 1, 1, 0): "9"
}

def gen():
    global output, last_trigger_time
    while True:
        success, frame = cam.read()
        if not success:
            continue
        hands, frame = detector.findHands(frame)
        text_to_display = "Try Again"

        if hands:
            hand = hands[0]
            fingerup = detector.fingersUp(hand)
            text_to_display = gestures.get(tuple(fingerup), "Try Again")

            current_time = time.time()
            if text_to_display != "Try Again" and (current_time - last_trigger_time) > cooldown_seconds:
                output = text_to_display
                last_trigger_time = current_time
                print(f"🎯 Gesture {output} detected!")

        # Encode frame to send to frontend
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template("index.html", output=output)

@app.route('/video')
def video():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reset', methods=['POST'])
def reset():
    global output
    output = ""
    return output


@app.route('/playlist1.html')
def playlist1():
    return render_template('playlist1.html')

@app.route('/playlist2.html')
def playlist2():
    return render_template('playlist2.html')

@app.route('/playlist3.html')
def playlist3():
    return render_template('playlist3.html')

@app.route('/playlist4.html')
def playlist4():
    return render_template('playlist4.html')

@app.route('/playlist5.html')
def playlist5():
    return render_template('playlist5.html')

@app.route('/playlist6.html')
def playlist6():
    return render_template('playlist6.html')

@app.route('/playlist7.html')
def playlist7():
    return render_template('playlist7.html')

@app.route('/playlist8.html')
def playlist8():
    return render_template('playlist8.html')

@app.route('/playlist9.html')
def playlist9():
    return render_template('playlist9.html')

@app.route('/playlist10.html')
def playlist10():
    return render_template('playlist10.html')

# 123
if __name__ == "__main__":
    app.run(debug=True)
