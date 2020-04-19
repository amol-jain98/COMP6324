import numpy as np
import argparse
import cv2
import time
import asyncio
import json
import base64
import os
import io
from converter import *
from distance import *
from objects import *
from warning import *
from time import sleep
from datetime import datetime
from playsound import playsound
from azure.iot.device.aio import IoTHubDeviceClient

# The azure device connection string
connection_string = "HostName=IoTGroup1StandardHub.azure-devices.net;DeviceId=dev001;SharedAccessKey=otK31C84fisZusMhtB4hQz4+EuMBcTxQCiJM/sIbbgU="
imageFileName = "imagefile.jpg"

async def main():

    # Device Initialisation
    device_client=IoTHubDeviceClient.create_from_connection_string(connection_string)
    await device_client.connect()
    webcam=cv2.VideoCapture(0)
    # Allow time for the camera to initialise
    sleep(2)
    COLORS=np.random.uniform(0, 255, size=(len(CLASSES), 3))

    net=cv2.dnn.readNetFromCaffe(
        'MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')
    log_buffer=[]
    iterations=1
    totalTime=0.0
    wflag=0

    warningSent={'1000': False, '500': False, '100': False}
    i=None
    prevTotalHazards=0

    while True:
        sleep(0.1)
        chk, image = webcam.read()
        sleep(0.2)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(
            image, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        start = time.time()
        detections = net.forward()
        end = time.time()
        totalTime = totalTime + (end - start)
        iterations = iterations + 1

        # Keep a count of the number of objects in the image, to be used later for TTS
        objectCount = {newList: 0 for newList in CLASSES}
        hazardCount = objectCount
        # Log to send out to azure
        log = {'date': datetime.now().strftime("%d/%m/%Y"),
                                  'time': datetime.now().strftime("%H:%M:%S"), 'images': [], 'hazardCount': 0, 'objectCount': objectCount}

        for i in np.arange(0, detections.shape[2]):
            confidence=detections[0, 0, i, 2]
            idx=int(detections[0, 0, i, 1])

            object=CLASSES[idx]
            if (inConfidenceRange(object, confidence)):
                box=detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY)=box.astype("int")
                kernel=np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])/9

                # For image encoding
                objectDetected=image.copy()
                objectDetected=objectDetected[startY:endY, startX:endX]
                cv2.imwrite(imageFileName, objectDetected)
                #log['images'].append("data:image/jpeg;base64," + str(convertfile(imageFileName)))

                focalLength=900
                width=endX - startX
                distance=distanceToCamera(object, focalLength, width)
                
                # Count the number of objects in the frame
                log['objectCount'][object] += 1            

                # Add detection to our count of objects if object is near
                if (distance < 1000):
                    hazardCount[object] += 1
                    
                label="{}: {:.2f}cm".format(CLASSES[idx], distance)
                log['hazardCount'] = sum(hazardCount.values())

                # send warning when obj is detected at less than 10m away & only send once for each threshold
                if((distance <= 1000) and (warningSent[str(findThreshold(distance))] == False)):
                    playsound(sendWarning(distance, object, warningSent, hazardCount))

                # send warning when another obj is detected
                if((distance <= 1000) and (prevTotalHazards > 0) and (log['hazardCount'] > prevTotalHazards)):
                    playsound(sendWarning(distance, object, warningSent, hazardCount))
                    
                # TODO: change to warning function
                if (distance < 250):
                    # Number of hazards detected in frame
                    log['hazardCount'] += 1

                # TODO: Check distance, then if within some threshold, play soundbyte

                cv2.rectangle(image, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y=startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, COLORS[idx], 1)

        if(log['hazardCount'] == 0):
            resetWarnings(warningSent)
        # record no. of hazards from previous img
        prevTotalHazards=log['hazardCount']

        cv2.imshow("Output", image)
        key=cv2.waitKey(1) & 0xFF

        async def send_data(data):
            await device_client.send_message(data)


        if (any(objectCount.values())):
            if (len(log_buffer) < 34):
                log_buffer.append(log)
            else:

                # We need to send out the data to microsoft azure as json
                json_body=json.dumps(log_buffer)
                log_buffer=[]
                await device_client.send_message(json_body)
                print("sent to azure")

        if (key == ord('q')):
            await device_client.disconnect()
            break


    cv2.destroyAllWindows()



if __name__ == "__main__":
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
