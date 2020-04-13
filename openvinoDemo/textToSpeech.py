import subprocess
import pyttsx3


# speaks here
def textToSpeech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# converts to wav file
def textToWav(text):
    subprocess.call(["espeak", "-w output.wav", text])
