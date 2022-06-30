from base64 import encode
import serial
from enum import unique
from sre_constants import SUCCESS
import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np
import time
import keyboard  
import math


#cap=cv2.VideoCapture('Files/Videos/vid (1).mp4')
cap=cv2.VideoCapture(0)
serialport= serial.Serial('COM4',9600)
#img=cv2.imread("Ball.png")

myColorFinder=ColorFinder(False)
hsvVals={'hmin': 112, 'smin': 72, 'vmin': 172, 'hmax': 173, 'smax': 255, 'vmax': 255}
posListX,posListY=[],[]
xL=[item for item in range(0,675)]
bc=[]

n=10  #number of contours(green dots)
i=0

while (True):
    try:  
        if keyboard.is_pressed(' '):  # if key 'q' is pressed 
            posListX.clear()
            posListY.clear()
            bc.clear()
            coord.clear()
        elif keyboard.is_pressed('w'):
             print(posListY[-1])    
        success, img=cap.read()
        imgColor, mask = myColorFinder.update(img,hsvVals)
        
        
# Find location of the ball
        imgContours, countours=cvzone.findContours(img,mask,minArea=10)
        if countours:
            # Stops when poslistX raches just before n
            if (len(posListX)<n):
                posListX.append(countours[0]['center'][0])
                posListY.append(countours[0]['center'][1])

            
        if posListX:
            A,B,C = np.polyfit(posListX,posListY,2)
            
            for (posx,posy) in zip(posListX,posListY):
                pos=(posx,posy)

                cv2.circle(imgContours,pos,5,(0,255,0),cv2.FILLED)           
             #   print(posListX)
            for x in xL:
                y=int(A*x*x+B*x+C)
                cv2.circle(imgContours,(x,y),3,(255,0,255),cv2.FILLED) 

                
# stored coordinates of trace in a dictionary
                coord={'xcr':x,'ycr':y}
                if (coord['ycr']==475):
                    p=coord['xcr']
                    bc.append(p)
                    if (len(bc)==4):                        
                        print(bc[-1])
                        serialport.write(bytes(f'{bc[-1]//20}','utf-8'))
                        print(f'{bc[-1]//20}')
                    
                        
                    cv2.line(imgContours,(p,0),(p,475),(0, 255, 0),2)
                #Soln-throw ball from a height such that only one pt for y=475
        #cv2.imshow("Image", img)
        cv2.imshow("ImageColor", imgContours)
        cv2.waitKey(1)
                
# if user pressed a key other than the given key the loop will break
    except:
        break
    