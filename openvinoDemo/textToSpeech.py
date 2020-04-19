import subprocess
from rmDir import rmDir

# This script creates wav files required for hazard notification
# Creates 3 folders: objectsWav, numbersWav, warningsWav
# If theses already exists, it is overwritten

# usage:
# from textToSpeech import createWavFiles
# createWavFiles()



# requires libespeak and espeak installed
# sudo apt-get install espeak
# sudo apt-get install -y libespeak-dev
# converts to wav file
def textToWav(text, folder):
    subprocess.call(["espeak", "-w " + folder + "/" + text + ".wav", text])

def makeFolder(foldername):
    subprocess.call(["mkdir", foldername])

def objectWavFiles():
    objects=["aeroplane", "background", "bicycle", "bird", "boat","bottle",
         "bus", "car", "cat", "chair", "cow", "diningtable", "dog", 
	     "horse", "motorbike", "person", "pottedplant", "sheep", "sofa",
	     "train", "tvmonitor"]

    rmDir("objectsWav")  
    makeFolder("objectsWav")
    for object in objects:
        textToWav(object, "objectsWav")

def numberWavFiles():
    rmDir("numbersWav")  
    makeFolder("numbersWav")
    for num in range(0,11):
        textToWav(str(num), "numbersWav")
        textToWav(str(num*10), "numbersWav")
        
def warningWavFiles():
    warnings=["Incoming", "Warning", "Hazard", "Approaching", "Metres Away", "And", "Detected", "No", "Danger"]
    rmDir("warningWav")  
    makeFolder("warningWav")
    for warning in warnings:
        textToWav(warning, "warningWav")     

def createWavFiles():
    objectWavFiles()
    numberWavFiles()
    warningWavFiles()

