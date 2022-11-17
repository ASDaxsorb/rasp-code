from flask import *
from camera import VideoCamera
import RPi.GPIO as GPIO

app = Flask(__name__)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.output(2, GPIO.LOW)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, GPIO.LOW)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.LOW)

video_camera = None
global_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def turn_off():
   print("Stop")
   GPIO.output(2, GPIO.LOW)
   GPIO.output(3, GPIO.LOW)
   GPIO.output(4, GPIO.LOW)
   GPIO.output(14, GPIO.LOW)
   
def set_direction(direction): 
   
   turn_off()

   if direction == "stop":
      return "Stopping"
   
   if direction == "up":
      GPIO.output(2, GPIO.HIGH)
      GPIO.output(4, GPIO.HIGH)
      print("Up")
   elif direction == "down":
      GPIO.output(3, GPIO.HIGH)
      GPIO.output(14, GPIO.HIGH)
      print("Down")
   elif direction == "left":
      GPIO.output(2, GPIO.HIGH)
      GPIO.output(14, GPIO.HIGH)
      print("Left")
   elif direction == "right":
      GPIO.output(3, GPIO.HIGH)
      GPIO.output(4, GPIO.HIGH)
      print("Right")
 
@app.route("/move", methods=["POST"])
def move():
   data = request.get_json()
   
   if data: 
      set_direction(data["direction"])
   
   return "Moving"

if __name__ == '__main__':
    host='192.168.100.89'
    app.run(host, threaded=True, debug=True)