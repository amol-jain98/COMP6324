from imutils.video import VideoStream
import numpy as np
import argparse
import time
import cv2
 
# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")
 
print("[INFO] starting video stream...")
webcam = cv2.VideoCapture(0)
print("Press Q to quit")

# loop over the frames from the video stream
while True:
    #frame = vs.read()
    ret, frame = webcam.read()
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (103.93, 116.77, 123.68)) 
    net.setInput(blob)
    detections = net.forward()
    count = 0    
    
    # loop over the detections
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if (confidence < 0.6) : #args["confidence"]:
            continue
        count += 1 
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        text = "{:.2f}%".format(confidence * 100) + ", Count " + str(count)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 255, 0), 1)
        cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
        
    # show the output frame
    cv2.imshow("Frame", frame)
 
    # if the `q` key was pressed, break from the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
 
# do a bit of cleanup
cv2.destroyAllWindows()
webcam.release()

