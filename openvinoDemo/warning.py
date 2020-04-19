from distance import *
from pydub import *
import time
from datetime import datetime

#creates custom warning msg
def makeWarningMsg(objectCount, obj, distanceFromCamera):
    #eg: warning 3 cars detected 5 metres away
    text = ("warning", objectCount[obj], obj, "detected", distanceFromCamera, "metres away" )
    combineWavFiles(obj, objectCount[obj]/100, distanceFromCamera)
 
#send warning 
def sendWarning(distanceFromUser, obj, warningCount, objectCount):
    distance = findThreshold(distanceFromUser)
    makeWarningMsg(objectCount, obj, distance)
    warningCount[str(distance)] = True
    
#defines hazard thresholds
def findThreshold(distanceFromUser):
    if (distanceFromUser <= 100):
        return 100
    #5m
    elif (distanceFromUser <= 500):
        return 500
    #10m
    elif (distanceFromUser <= 1000):
        return 1000
        
#reset warnings when no obstaces are detected
def resetWarnings(warningCount):
    for warning in warningCount:
        warningCount[warning] = False

# $ sudo apt-get install python-pip
# $ pip3 install pydub
def combineWavFiles(object, objectCount, distanceAway):
    now = datetime.now().strftime("%Y-%m-%d,%H:%M")
    
    #eg: warning 3 cars detected 5 metres away
    warning = AudioSegment.from_wav("./warningWav/Warning.wav")
    detected = AudioSegment.from_wav("./warningWav/Detected.wav")
    metresAway = AudioSegment.from_wav("./warningWav/Metres Away.wav")
    
    objCount = AudioSegment.from_wav("./numbersWav/" + str(objectCount) + ".wav")
    obj = AudioSegment.from_wav("./objectsWav/" + object + ".wav")
    distance = AudioSegment.from_wav("./numbersWav/" + str(distanceAway) + ".wav")

    customMsg = warning + objCount + obj + detected + distance + metresAway
    customMsg.export("customWarning" + now + ".wav", format="wav")
        
