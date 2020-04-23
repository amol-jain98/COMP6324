from distance import *
from pydub import *
import time
from datetime import datetime
from playsound import playsound
from pyplay import SoundPlayer

#creates custom warning msg
def makeWarningMsg(objectCount, obj, distanceFromCamera):
    #eg: warning 3 cars detected 5 metres away
    text = (objectCount[obj], obj, distanceFromCamera, "meters" )
    return combineWavFiles(obj, objectCount[obj], distanceFromCamera//100)
 
#send warning 
def sendWarning(distanceFromUser, obj, warningCount, objectCount):
    player = SoundPlayer()
    distance = findThreshold(distanceFromUser)
    filename = makeWarningMsg(objectCount, obj, distance)
    warningCount[str(distance)] = True
    player.play(filename)
    
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
    metres = AudioSegment.from_wav("./warningWav/Metres Away.wav")
    
    objCount = AudioSegment.from_wav("./numbersWav/" + str(objectCount) + ".wav")
    obj = AudioSegment.from_wav("./objectsWav/" + object + ".wav")
    distance = AudioSegment.from_wav("./numbersWav/" + str(distanceAway) + ".wav")

    customMsg = objCount + obj + distance + metres
    filename = "warnings/customWarning" + now + ".wav"
    customMsg.export(filename, format="wav")
    return filename
