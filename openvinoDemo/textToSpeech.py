import subprocess
from objects import *

# This script creates wav files required for hazard notification
# Creates 3 folders: objectsWav, numbersWav, warningsWav

# requires libespeak and espeak installed
# sudo apt-get install espeak
# sudo apt-get install -y libespeak-dev
# converts to wav file

warnings=["Incoming", "Warning", "Hazard", "Approaching", "Metres Away", "And", "Detected", "No"]

def textToWav(text, folder):
    subprocess.call(["espeak", "-w " + folder + "/" + text + ".wav", text])

def makeFolder(foldername):
    subprocess.call(["mkdir", foldername])

def objectWavFiles():
    objects=CLASSES

    makeFolder("objectsWav")
    for object in objects:
        textToWav(object, "objectsWav")

def numberWavFiles():
    makeFolder("numbersWav")
    for num in range(0,11):
        textToWav(str(num), "numbersWav")
        textToWav(str(num*10), "numbersWav")
        
def warningWavFiles():
    makeFolder("warningWav")
    for warning in warnings:
        textToWav(warning, "warningWav")     
    
objectWavFiles()
numberWavFiles()
warningWavFiles()
