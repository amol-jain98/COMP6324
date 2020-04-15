import subprocess
#import pyttsx3

# This script creates wav files required for hazard notification
# Creates 3 folders: objectsWav, numbersWav, warningsWav

# requires pyttsx3 pip3 installed
# speaks here
#def textToSpeech(text):
#    engine = pyttsx3.init()
#    engine.say(text)
#    engine.runAndWait()
#    engine.stop()


# requires libespeak and espeak installed
# sudo apt-get install espeak
# sudo apt-get install -y libespeak-dev
# converts to wav file
def textToWav(text, folder):
    subprocess.call(["espeak", "-w " + folder + "/" + text + ".wav", text])

def makeFolder(foldername):
    subprocess.call(["mkdir", foldername])

def objectWavFiles():
    objects=["bicycle", "bird", "boat","bottle", "bus", "car", 
	     "cat", "chair", "cow", "diningtable", "dog", 
	     "horse", "motorbike", "person", "pottedplant", 
	     "sheep", "sofa", "train", "tvmonitor"]

    makeFolder("objectsWav")
    for object in objects:
        textToWav(object, "objectsWav")

def numberWavFiles():
    makeFolder("numbersWav")
    for num in range(0, 11):
        textToWav(num, "rangesWav")
    numbers=[20, 30, 40, 50, 60, 70, 80, 90, 100]
    for num in numbers:
	textToWav(num, "rangesWav")
        
def warningWavFiles():
    warnings=["Incoming", "Warning", "Hazard", "Approaching", "Metres Away", "And", "Detected", "No"]
    makeFolder("warningWav")
    for warning in warnings:
        textToWav(warning, "warningWav")     
    
objectWavFiles()
numberWavFiles()
warningWavFiles()
