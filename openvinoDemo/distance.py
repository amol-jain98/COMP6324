import time

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
    

