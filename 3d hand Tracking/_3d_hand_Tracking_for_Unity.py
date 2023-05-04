import math
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import socket
import numpy

#parameters
width, height = 1280, 720

#WebCam
cap = cv2.VideoCapture(1)
cap.set(3, width,)
cap.set(4, height)

#Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.85)

#find function coeff to calculate rough distance between hand and a camera
#x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
#y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
#coff = numpy.polyfit(x, y, 2)



#communication part
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

#sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#serverAddressPort2 = ("127.0.0.1", 3052)

while True:

    #Get the frame from the webcam
    success, img = cap.read()
    #Hands
    hands, img = detector.findHands(img)

    data = [] #reset it every iteration

    #Landmark values-(x,y,z) * 21 in a single list
    if hands:
        #Get the first hand detected
        hand = hands[0]

        # Get the landmark list

        lmList = hand['lmList']
       # x, y, w, h = hand['bbox']
       # x1, y1, z1 = lmList[5]
       # x2, y2, z2 = lmList[17]


        #distance = int(math.sqrt((y2-y1) **2 + (x2-x1)**2))
       # A, B, C = coff

       # distanceCM = A*distance **2 + B*distance + C

        #print(lmList)
        #print(distanceCM, distance)
        #cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10))
        for lm in lmList:
            data.extend([lm[0], height-lm[1], lm[2]])

        #print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)
        #sock.sendto(str.encode(str(lmList)), serverAddressPort)
        #sock2.sendto(str.encode(str(distanceCM)), serverAddressPort2)


        img = cv2.resize (img, (0,0), None, 0.75, 0.75)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

