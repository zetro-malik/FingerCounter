import cv2
import time
import os
import HandTrackingModule as htm


Ptime = 0
Ctime = 0

wCam, hCam = 640,480

detector = htm.HandDetector(detectionCon=0.75)

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

lstHands = []

for imgpath in os.listdir(os.path.join("Resources")):
    img=cv2.imread(os.path.join("Resources"+"/"+imgpath))
    img = cv2.resize(img,(200,200),interpolation=cv2.INTER_AREA)
    lstHands.append(img)


tipIds = [4 ,8, 12, 16, 20]

while True:

    #reading Frame
    success, img = cap.read()
    img = cv2.flip(img ,1)

    #couting algorithm
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)

    if len(lmlist) !=0:
        fingers = []   

        # thumb
        if lmlist[tipIds[0]][1] < lmlist[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 for fingers
        for id in range(1, 5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        cv2.putText(img,str(F"Count: {totalFingers}"),(10,300),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),5)

        # adding hand image in live video
        w,h,c =lstHands[totalFingers].shape
        img[0:w,0:h] = lstHands[totalFingers] 

    

    #showing FPS
    Ctime = time.time()
    fps = 1/(Ctime-Ptime)
    Ptime=Ctime

    cv2.putText(img,str(F"FPS: {int(fps)}"),(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),5)


    cv2.imshow("Image",img)

    cv2.waitKey(1)