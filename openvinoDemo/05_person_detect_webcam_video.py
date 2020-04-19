import numpy as np
import argparse
import cv2
import time
import asyncio
import json
import os
from converter import *
from distance import *
from objects import *
from warning import *
from time import sleep
from datetime import datetime
from azure.iot.device.aio import IoTHubDeviceClient

# The azure device connection string
connection_string = "HostName=IoTGroup1StandardHub.azure-devices.net;DeviceId=dev001;SharedAccessKey=otK31C84fisZusMhtB4hQz4+EuMBcTxQCiJM/sIbbgU="


def confident(object, confidence):
    return (confidence > 0.4 and (object is 'person' or object is 'car' or object is 'bicycle')) or (confidence > 0.5 and object is 'motorbike') or (confidence > 0.7 and (object is 'train' or object is 'bus')


async def initialiseIoTDevice():
    device_client=IoTHubDeviceClient.create_from_connection_string(
        connection_string)
    await device_client.connect()

async def main():
    webcam=cv2.VideoCapture(0)
    # Allow time for the camera to initialise

    sleep(2)
    COLORS=np.random.uniform(0, 255, size=(len(CLASSES), 3))

    net=cv2.dnn.readNetFromCaffe(
        'MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')
    initialiseAzure()
    log_buffer=[]
    iterations=1
    totalTime=0.0
    wflag=0

    warningSent={'1000': False, '500': False, '100': False}
    i=None
    prevTotalHazards=0

    while True:
        sleep(0.1)
        chk, image=webcam.read()
        sleep(0.2)
        (h, w)=image.shape[:2]
        blob=cv2.dnn.blobFromImage(cv2.resize(
            image, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        start=time.time()
        detections=net.forward()
        end=time.time()
        totalTime=totalTime + (end - start)
        totalHazards=0
        iterations=iterations + 1

        # Keep a count of the number of objects in the image, to be used later for TTS
        objectCount={newList: 0 for newList in CLASSES}
        # Log to send out to azure
        log={'date': datetime.now().strftime("%d/%m/%Y"),
                                  'time': datetime.now().strftime("%H:%M:%S"), 'images': [], 'hazardCount': 0}
        log.update(objectCount)

        for i in np.arange(0, detections.shape[2]):
            confidence=detections[0, 0, i, 2]
            idx=int(detections[0, 0, i, 1])

            object=CLASSES[idx]
            if (confident(object, confidence):
                box=detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY)=box.astype("int")
                kernel=np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])/9

                objectDetected=image.copy()
                objectDetected=objectDetected[startY:endY, startX:endX]
                outfile="{}{}{}.jpg".format(i, CLASSES[idx], now)
                cv2.imwrite(outfile, objectDetected)
                convertfile(i, CLASSES[idx], now)
                os.remove(outfile)

                focalLength=900
                width=endX - startX
                distance=distanceToCamera(object, focalLength, width)

                # # Add detection to our count of objects if object is near
                if (distance < 1000):
                objectCount[object] += 1
                label="{}: {:.2f}cm".format(CLASSES[idx], distance)
                totalHazards=totalHazardCount(objectCount)

                # send warning when obj is detected at less than 10m away & only send once for each threshold
                if((distance <= 1000) and (warningSent[str(findThreshold(distance))] == False)):
                    sendWarning(distance, object, warningSent, objectCount)

                # send warning when another obj is detected
                if((distance <= 1000) and (prevTotalHazards > 0) and (totalHazards > prevTotalHazards)):
                    sendWarning(distance, object, warningSent, objectCount)

                # Objects detected in frame
                objectCount[object] += 1

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


                # send warning when another obj is detected
                if((distance <= 1000) and (prevTotalHazards > 0) and (totalHazards > prevTotalHazards)):
                sendWarning(distance, object, warningSent, objectCount)

                # TODO: Add actual image data
                log["images"].append(
                    "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/4QPMRXhpZgAASUkqAAgAAAAIAA4BAgCVAAAAbgAAAA8BAgAGAAAABAEAABABAgAPAAAACgEAADsBAgA")

        if(totalHazards == 0):
            resetWarnings(warningSent)
        # record no. of hazards from previous img
        prevTotalHazards=totalHazards

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
