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
    KNOWN_WIDTH = 0
    if objectIdentity == 'car':
        #in cms
        KNOWN_WIDTH=185
    if objectIdentity == 'person':
        KNOWN_WIDTH=30
    return KNOWN_WIDTH

webcam = cv2.VideoCapture(0)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("loading Caffe SSD MobileNet Model...")
net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

iterations = 1
total_time = 0.0
wflag = 0
while True:
    sleep(0.3)
    chk, image = webcam.read()
    sleep(0.2)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    start = time.time()
    detections = net.forward()
    end = time.time()
    total_time = total_time + (end - start)
    #print('avg = ', end-start)
    iterations = iterations + 1
    for i in np.arange(0, detections.shape[2]):
        print("0")
        confidence = detections[0, 0, i, 2]
        print("1")
        idx = int(detections[0, 0, i, 1])
        if (confidence > 0.4) and (CLASSES[idx] == 'person' or CLASSES[idx] == 'car' or CLASSES[idx] == 'bicycle' or CLASSES[idx] == 'bus' or CLASSES[idx] == 'train' or CLASSES[idx] == 'motorbike'):
            #or 
            #(confidence > 0.6 and (CLASSES[idx] == 'bottle' or 
            #CLASSES[idx] == 'chair' or CLASSES[idx] == 'sofa' or CLASSES[idx] == 'diningtable'):
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            person = image.copy()
            person = person[startY:endY, startX:endX]
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])/9

#            sharp_person = cv2.filter2D(person, -1, kernel)
            focalLength = 900
            width = endX - startX
            distance = distanceToCamera(CLASSES[idx], focalLength, width)
            label = "{}: {}".format(CLASSES[idx], distance)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.3, COLORS[idx], 1)
    cv2.imshow("Output", image)
    key = cv2.waitKey(1) & 0xFF
    if (key == ord('q')):
        break
               
cv2.destroyAllWindows()
