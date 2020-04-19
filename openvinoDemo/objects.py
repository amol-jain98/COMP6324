CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]


def initializationMeasurements(objectIdentity):
    # The known width of the objects in centimeters
    knownWidth = {'car': 185, 'person': 40, 'bicycle': 40, 'motorbike': 40, 
                    'train': 300, 'bus': 300, 'background': 0, 'aeroplane': 6000, 'bird': 22, 'boat': 185,
	    'bottle': 7, 'cat': 18, 'chair': 38, 'cow': 0, 'diningtable': 0,
	    'dog': 0, 'horse': 0, 'pottedplant': 0, 'sheep': 0,
	    'sofa': 0, 'tvmonitor': 0 }      
    return knownWidth[objectIdentity]	


# Set the confidence range for different objs
def inConfidenceRange(obj, confidence):
    if ((confidence > 0.4) and (obj == 'person' or obj == 'car' or obj == 'bicycle')):
        return True
    elif (confidence > 0.5 and obj == 'motorbike') or (confidence > 0.7 and (obj == 'train' or obj == 'bus')):
        return True
    elif ((confidence > 0.6) and (obj == 'bottle' or obj == 'chair' or obj == 'sofa' or obj == 'diningtable' or obj == 'tvmonitor')):
        return True
    elif ((confidence > 0.4) and (obj == 'background' or obj == 'aeroplane' or obj == 'bird' or obj == 'boat' or obj == 'cat' or obj == 'cow' or obj == 'dog' or obj == 'horse' or obj == 'pottedplant' or obj == 'sheep')):
        return True
    else:
        return False

#find out how many hazards there are altogether
def totalHazardCount(objectCount):
    total = 0
    for obj in objectCount:
        total += objectCount[obj]
    return total
    
    
