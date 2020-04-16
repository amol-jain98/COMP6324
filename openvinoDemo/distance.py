import time

def distanceToCamera(identity,focalLength, width):
	# compute and return the distance from the maker to the camera
	return (initializationMeasurements(identity) * focalLength) / width
	
def initializationMeasurements(objectIdentity):
    # The known length of the objects in centimeters
    knownLength = {'car': 185, 'person': 30, 'bicycle': 170, 'motorbike': 190, 
                    'train': 1700, 'bus': 1250}      
    return knownLength[objectIdentity]
'''
def initializationMeasurements(objectIdentity):
    KNOWN_WIDTH = 0
    if objectIdentity == 'car':
        #in cms
        KNOWN_WIDTH=7
    if objectIdentity == 'person':
        KNOWN_WIDTH=30
    return KNOWN_WIDTH
    
'''
