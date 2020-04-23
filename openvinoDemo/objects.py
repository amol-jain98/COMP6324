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
    confidences = {'person': 0.6, 'car': 0.7, 'bicycle': 0.6, 'motorbike': 0.6, 'train': 0.9, 'bus': 0.7, 'bottle': 0.8, 'chair': 0.8, 'sofa': 0.8, 'diningtable': 0.9, 'tvmonitor': 0.9, 'background': 0.9, 'aeroplane': 0.9}

    if obj in confidences.keys():
        return confidence > confidences[obj]
    return False

