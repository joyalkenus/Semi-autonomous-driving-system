from multiprocessing.connection import wait
import numpy as np
import dlib
import cv2
import serial
import time


cap = cv2.VideoCapture(1)




down ="b"
up="f"
left="l"
right="r"
stop="s"
buffer=[]


# Start communications with the bluetooth unit
bluetooth = serial.Serial('COM9', 9600)
bluetooth.timeout=1

detector = dlib.get_frontal_face_detector()
predictor= dlib.shape_predictor("shape_68_lmarks.dat")


while True:
    
    buffer += [chr(c) for c in bluetooth.read(2)]
    
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        x1=face.left()
        y1=face.top()
        x2= face.right()
        y2= face.bottom()
        #cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)



        landmarks= predictor(gray,face)
        list = [2,14,30,47,40]
        list2 =[52,58]
        for i in range(0,68):
            x = landmarks.part(i).x
            y= landmarks.part(i).y
            cv2.circle(frame, (x,y), 3, (0, 255, 0), -1)
        
       #distance(landmarks.part(14).x,landmarks.part(14).y,landmarks.part(30).x,landmarks.part(30).y)
        v1 = landmarks.part(30).y #nose
        v2 = landmarks.part(14).y #left ear in image
        m1= landmarks.part(52).y
        m2= landmarks.part(58).y
        difm=m2-m1

        dif = v2-v1
        h0= landmarks.part(30).x
        h1 = landmarks.part(40).x
        h2 = landmarks.part(47).x
        hleft = h2-h0                      
        hright = h0-h1
        
        
        
        if dif < -10: # condition for face looking down
            
            cv2.putText(frame,'backward',(50, 50),cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 255, 255),2,cv2.LINE_4)
            down.strip()            
            bluetooth.write(down.encode())
            
            
            
            

        elif -10 < dif < 40: # condition for face looking in the middle section
            
            

            if hleft < 11:

                cv2.putText(frame,
                            'left',
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 255),
                            2   ,
                            cv2.LINE_4)
                left.strip()
                bluetooth.write(left.encode())
               
                

            elif hright < 11:

                cv2.putText(frame,
                            'right',
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 255),
                            2,
                            cv2.LINE_4)
                right.strip()
                bluetooth.write(right.encode())
                
            else:
                stop.strip()
                bluetooth.write(stop.encode())
               
                
                
                

        elif dif > 38:

            cv2.putText(frame,
                        'forward',
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)
            up.strip()
            bluetooth.write(up.encode())
           
            


    cv2.imshow("face orientation system",frame)
    
    
    
    key=cv2.waitKey(1)
    if key==27:
        break
    
    
