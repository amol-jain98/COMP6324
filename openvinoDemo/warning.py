from distance import *

#creates custom warning msg using sound files
def makeWarningMsg(obj, quantity, distanceFromCamera):
    return 0
    
#send warning to user 
#send warning based on w
def sendWarning(distanceFromUser, obj, warningCount):
    print("obstacle in", findThreshold(distanceFromUser), "cm")
    warningCount[str(findThreshold(distanceFromUser))] = True

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
