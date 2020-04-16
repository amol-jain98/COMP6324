import numpy as np
import argparse
import cv2
import time
from time import sleep
from timeout import timeout

def distanceToCamera(identity,focalLength, width):
	# compute and return the distance from the maker to the camera
	return (initializationMeasurements(identity) * focalLength) / width

def initializationMeasurements(objectIdentity):
    # The known length of the objects in centimeters
    knownLength = {'car': 185, 'person': 30, 'bicycle': 170, 'motorbike': 190, 
                    'train': 1700, 'bus': 1250}      
    return knownLength[objectIdentity]

webcam = cv2.VideoCapture(0)
# Allow time for the camera to initialise

sleep(2)
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

iterations = 1
totalTime = 0.0
wflag = 0

while True:
    sleep(0.2)
    chk, image = webcam.read()
    sleep(0.1)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    start = time.time()
    detections = net.forward()
    end = time.time()
    totalTime = totalTime + (end - start)
    #print('avg = ', end-start)
    iterations = iterations + 1
    
    # Keep a count of the number of objects in the image, to be used later for TTS
    objectCount = {'person': 0, 'car': 0, 'bicycle': 0, 'bus': 0, 'motorbike': 0, 'train': 0}
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        idx = int(detections[0, 0, i, 1])
        object = CLASSES[idx]
        if ((confidence > 0.4) and (object == 'person' or object == 'car' or object == 'bicycle')) or (confidence > 0.5 and object == 'motorbike') or (confidence > 0.7 and (object == 'train' or object == 'bus')):
            #or 
            #(confidence > 0.6 and (CLASSES[idx] == 'bottle' or 
            #CLASSES[idx] == 'chair' or CLASSES[idx] == 'sofa' or CLASSES[idx] == 'diningtable'):
            
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])/9

            # Check distance, then if within some threshold, play soundbyte
            focalLength = 900
            width = endX - startX
            distance = distanceToCamera(CLASSES[idx], focalLength, width)
            
            # Add detection to our count of objects if object is near
            if (distance < 250):
                objectCount[object] += 1
            label = "{}: {}".format(CLASSES[idx], distance)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.3, COLORS[idx], 1)
    if (any(objectCount.values())):
        print(objectCount)
    cv2.imshow("Output", image)
    key = cv2.waitKey(1) & 0xFF
    if (key == ord('q')):
        break
               
cv2.destroyAllWindows()
