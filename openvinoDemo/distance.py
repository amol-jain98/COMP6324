from objects import *

def distanceToCamera(identity,focalLength, width):
	# compute and return the distance from the maker to the camera
	return (initializationMeasurements(identity) * focalLength) / width	

#checks if obj is approaching the camera 
def approachingCamera(curDist, prevDist):
    #if obj has moved more than 20cms since last detection, it is approaching
    if (prevDist == None):
        return False
    return True if  (curDist < prevDist - 20) else False

