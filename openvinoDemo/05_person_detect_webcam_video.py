import numpy as np
import argparse
import cv2
import time
import os
from datetime import datetime
from converter import *
from distance import *
from objects import *
from warning import *
from time import sleep

webcam = cv2.VideoCapture(0)
# Allow time for the camera to initialise

sleep(2)
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

iterations = 1
totalTime = 0.0
wflag = 0
warningSent = {'1000': False, '500': False, '100': False}
i = None
prevTotalHazards = 0

while True:
    sleep(0.1)
    chk, image = webcam.read()
    sleep(0.1)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    start = time.time()
    detections = net.forward()
    end = time.time()
    totalTime = totalTime + (end - start)
    totalHazards = 0
    iterations = iterations + 1
    
    # Keep a count of the number of objects in the image, to be used later for TTS
    now = datetime.now().strftime("%Y-%m-%d,%H:%M")
    objectCount = {'background': 0, 'aeroplane': 0, 'bicycle': 0, 'bird': 0, 'boat': 0,
	    'bottle': 0, 'bus': 0, 'car': 0, 'cat': 0, 'chair': 0, 'cow': 0, 'diningtable': 0,
	    'dog': 0, 'horse': 0, 'motorbike': 0, 'person': 0, 'pottedplant': 0, 'sheep': 0,
	    'sofa': 0, 'train': 0, 'tvmonitor': 0 }
                
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        idx = int(detections[0, 0, i, 1])
        object = CLASSES[idx]        
        if (inConfidenceRange(object, confidence)):
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])/9
            
            #for base64
            objectDetected = image.copy()
            objectDetected = objectDetected[startY:endY, startX:endX]
            outfile = "{}{}{}.jpg".format(i,CLASSES[idx],now)            
            cv2.imwrite(outfile, objectDetected)
            convertfile(i,CLASSES[idx],now)
            os.remove(outfile)
            
            focalLength = 900
            width = endX - startX
            distance = distanceToCamera(CLASSES[idx], focalLength, width)

            # Add detection to our count of objects if object is near
            if (distance < 1000):
                objectCount[object] += 1
            label = "{}: {:.2f}cm".format(CLASSES[idx], distance)
            totalHazards = totalHazardCount(objectCount)
            print("obj is", object)
            #send warning when obj is detected at less than 10m away & only send once for each threshold
            if((distance <= 1000) and (warningSent[str(findThreshold(distance))] == False)):
                sendWarning(distance, object, warningSent, objectCount)
                
            #print("total", totalHazards, "hazards detected")
            
            #send warning when another obj is detected 
            if((distance <= 1000) and (prevTotalHazards > 0 ) and (totalHazards > prevTotalHazards)):
                print(object)
                print("total", totalHazards, "prevTotal", prevTotalHazards)
                sendWarning(distance, object, warningSent, objectCount)
                
            #TODO:
            #make custom wav file
            #send to bluetooth device

            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.3, COLORS[idx], 1)  
            
    if(totalHazards == 0):
        resetWarnings(warningSent)
    
    #record no. of hazards from previous img
    prevTotalHazards = totalHazards
        
    cv2.imshow("Output", image)
    key = cv2.waitKey(1) & 0xFF
    if (key == ord('q')):
        break
               
cv2.destroyAllWindows()
