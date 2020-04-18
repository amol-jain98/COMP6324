import numpy as np
import argparse
import cv2
import time
import asyncio
import json
from distance import *
from classes import *
from warning import *
from time import sleep
from datetime import datetime
from azure.iot.device.aio import IoTHubDeviceClient

async def main():
    webcam = cv2.VideoCapture(0)
    # Allow time for the camera to initialise

    sleep(2)
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')
    connection_string = "HostName=IoTGroup1StandardHub.azure-devices.net;DeviceId=dev001;SharedAccessKey=otK31C84fisZusMhtB4hQz4+EuMBcTxQCiJM/sIbbgU=" # The azure device connection string
    device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    await device_client.connect()
    log_buffer = []
    iterations = 1
    totalTime = 0.0
    wflag = 0
    firstLoop = False

    while True:
        sleep(0.1)
        chk, image = webcam.read()
        sleep(0.2)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        start = time.time()
        detections = net.forward()
        end = time.time()
        totalTime = totalTime + (end - start)
        #print('avg = ', end-start)
        #print('total = ', total_time)
        iterations = iterations + 1
        
        # Keep a count of the number of objects in the image, to be used later for TTS
        hazardCount = 0
        objectCount = {'person' : 0 , 'car' : 0 , 'bicycle' : 0 , 'motorbike':0,'train' :0 , 'bus':0}
        # Log to send out to azure
        log = {'date': datetime.now().strftime("%d/%m/%Y"), 'time': datetime.now().strftime("%H:%M:%S"), 'images':[], 'person' : 0 , 'car' : 0 , 'bicycle' : 0 , 'motorbike':0,'train' :0 , 'bus':0,'hazardCount': hazardCount}
            
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            idx = int(detections[0, 0, i, 1])
            
            object = CLASSES[idx]
            if (confidence > 0.4 and (object == 'person' or object == 'car' or object == 'bicycle')) or (confidence > 0.5 and object == 'motorbike') or (confidence > 0.7 and (object == 'train' or object == 'bus')):
            #or 
                #(confidence > 0.6 and (CLASSES[idx] == 'bottle' or 
                #CLASSES[idx] == 'chair' or CLASSES[idx] == 'sofa' or CLASSES[idx] == 'diningtable'):

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])/9
                
                focalLength = 900
                width = endX - startX
                distance = distanceToCamera(CLASSES[idx], focalLength, width)
                
                #store distance of obj from camera when first detected
                if (firstLoop == False):
                    startDistance = distance
                    firstLoop = True
                    
                travelledDistance = startDistance - distance
                speed = travelledDistance/(totalTime)
                #print('distance, Travelled, start', distance, travelledDistance, startDistance)
                
                # Objects detected in frame
                objectCount[object] += 1
                
                #TODO: change to warning function
                if (distance < 250):
                    # Number of hazards detected in frame
                    log[object] += 1
                    hazardCount++
                  
                label = "{}: {:.2f}cm, {:.2f}cm/s".format(CLASSES[idx], distance, travelledDistance)

                #TODO: Check distance, then if within some threshold, play soundbyte
                
                cv2.rectangle(image, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, COLORS[idx], 1)

                 
                #TODO: Add actual image data
                log["images"].append("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/4QPMRXhpZgAASUkqAAgAAAAIAA4BAgCVAAAAbgAAAA8BAgAGAAAABAEAABABAgAPAAAACgEAADsBAgA")
        
                log["hazard"] = sum(hazardCount)
        cv2.imshow("Output", image)
        key = cv2.waitKey(1) & 0xFF
        
        async def send_data(data):
            await device_client.send_message(data)

        
        if (any(objectCount.values())):
            if (len(log_buffer) < 34):
                log_buffer.append(log)
            else:
            
                # We need to send out the data to microsoft azure as json
                json_body = json.dumps(log_buffer)
                log_buffer = []
                await device_client.send_message(json_body)
                print("sent to azure")     
            
        if (key == ord('q')):
            device_client.disconnect()
            break
        
                   
    cv2.destroyAllWindows()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
