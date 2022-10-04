import os
import cv2
import threading
import time
import datetime

class RecordingThread (threading.Thread):
    def __init__(self, name, camera):
        video_path = r'./static/video.avi'
        if os.path.exists(video_path):
            os.remove(video_path)
            
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True
        
        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 0)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
    
            h = 640
            frame = cv2.putText(frame, now,
                                (10, h - 30),
                                font, 1,
                                (255, 255, 255),
                                2, cv2.LINE_8)
                
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.start_time = time.time()
        self.cap = cv2.VideoCapture(0)

        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 0)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
    
        h = 640
        current = time.gmtime(time.time() - self.start_time)
        current = time.strftime("%H:%M:%S", current)
        frame = cv2.putText(frame, now,
                            (10, h - 30),
                            font, 1,
                            (255, 255, 255),
                            2, cv2.LINE_8)
        if self.is_record:
            frame = cv2.putText(frame, current,
                                (10, h - 90),
                                font, 1,
                                (255, 255, 255),
                                2, cv2.LINE_8)

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))
                
            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None  

            return jpeg.tobytes()
      
        else:
            return None

    def start_record(self):
        self.start_time = time.time()
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread != None:
            self.recordingThread.stop()

            
