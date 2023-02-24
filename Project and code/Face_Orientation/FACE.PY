from multiprocessing.connection import wait
import numpy as np
import dlib
import cv2
import serial
import time


cap = cv2.VideoCapture(1)


down = "b"
up = "f"
left = "l"
right = "r"
stop = "s"
buffer = []

port = "COM3"
# Start communications with the bluetooth unit
bluetooth = serial.Serial('COM9', 9600)
bluetooth.timeout = 1
bluetooth.flushInput()

bluetooth.reset_input_buffer()
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_68_lmarks.dat")
while True:

    

    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        #cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
        landmarks = predictor(gray, face)
        list = [2, 14, 30, 47, 40]
        for i in list:
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        #distance(landmarks.part(14).x,landmarks.part(14).y,landmarks.part(30).x,landmarks.part(30).y)
        v1 = landmarks.part(30).y  # nose
        v2 = landmarks.part(14).y  # left ear in image
        dif = v2-v1
        h0 = landmarks.part(30).x
        h1 = landmarks.part(40).x
        h2 = landmarks.part(47).x
        hleft = h2-h0
        hright = h0-h1

        if dif < -10:

            cv2.putText(frame,
                        'down',
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)
            down.strip()
            bluetooth.write(down.encode())
            bluetooth.readline().decode()

        elif -10 < dif < 40:

            if hleft < 6:

                cv2.putText(frame,
                            'left',
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 255),
                            2,
                            cv2.LINE_4)
                left.strip()
                bluetooth.write(left.encode())
                bluetooth.readline().decode()

            elif hright < 6:

                cv2.putText(frame,
                            'right',
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 255),
                            2,
                            cv2.LINE_4)
                right.strip()
                bluetooth.write(right.encode())
                bluetooth.readline().decode()

            else:
                stop.strip()
                bluetooth.write(stop.encode())
                bluetooth.readline().decode()

        elif dif > 38:

            cv2.putText(frame,
                        'up',
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)
            up.strip()
            bluetooth.write(up.encode())
            bluetooth.readline().decode()

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
