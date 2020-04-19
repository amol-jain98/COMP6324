import subprocess
from objects import *
from rmDir import rmDir

# This script creates wav files required for hazard notification
# Creates 3 folders: objectsWav, numbersWav, warningsWav
# If theses already exists, it is overwritten

# usage:
# from textToSpeech import *
# createWavFiles()

# requires libespeak and espeak installed
# sudo apt-get install espeak
# sudo apt-get install -y libespeak-dev
# converts to wav file

warnings=["Incoming", "Warning", "Hazard", "Approaching", "Metres Away", "And", "Detected", "No", "Danger"]

def textToWav(text, folder):
    subprocess.call(["espeak", "-w " + folder + "/" + text + ".wav", text])

def makeFolder(foldername):
    subprocess.call(["mkdir", foldername])

def objectWavFiles():
    objects=CLASSES
    rmDir("objectsWav")  
    makeFolder("objectsWav")
    for object in objects:
        textToWav(object, "objectsWav")

def numberWavFiles():
    rmDir("numbersWav")  
    makeFolder("numbersWav")
    textToWav("Hundred", "numbersWav")
    for num in range(0,20):
        textToWav(str(num), "numbersWav")
        if num < 10:
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

