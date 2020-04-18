from distance import *

#creates custom warning msg
def makeWarningMsg(objectCount, obj, distanceFromCamera):
    #eg: warning 3 cars detected 5 metres away
    print("warning", objectCount[obj], obj, "detected", distanceFromCamera, "metres away" )
 
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
           
#send warning when warning has not been sent
#reset warning to false when no obstacles are detected 
#when new obj is detected, send warning regardless of what the dictionary says
