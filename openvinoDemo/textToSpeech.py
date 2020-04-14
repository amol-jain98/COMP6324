import subprocess
#import pyttsx3

# This file creates wav files required for hazard notification

# requires pyttsx3 pip3 installed
# speaks here
#def textToSpeech(text):
#    engine = pyttsx3.init()
#    engine.say(text)
#    engine.runAndWait()
#    engine.stop()


# requires libspeak and espeak installed
# sudo apt-get install espeak
# sudo apt-get install -y libespeak-dev
# converts to wav file
def textToWav(text, folder):
    subprocess.call(["espeak", "-w " + folder + "/" + text + ".wav", text])

def makeFolder(foldername):
    subprocess.call(["mkdir", foldername])

def objectWavFiles():
    objects=["bicycle", "bird", "boat",
	    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	    "sofa", "train", "tvmonitor"]

    makeFolder("objects")
    for object in objects:
        textToWav(object, "objects")

def rangeWavFiles():
    ranges=["1", "2", "3", "4"]
    makeFolder("ranges")
    for range in ranges:
        textToWav(range+" Metres Away", "ranges")
        
def warningWavFiles():
    warnings=["Incoming", "Warning", "Hazard", "Approaching"]
    makeFolder("warning")
    for warning in warnings:
        textToWav(warning, "warning")     
    
objectWavFiles()
rangeWavFiles()
warningWavFiles()
