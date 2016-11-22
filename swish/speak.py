import os

from gtts import gTTS
from pygame import mixer

FILENAME = "response.mp3"

mixer.init()


def speak(response, save=False):
    tts = gTTS(text=response, lang="en")

    tts.save(FILENAME)

    mixer.music.load(FILENAME)
    mixer.music.play()

    while mixer.music.get_busy():
        pass

    if not save:
        os.remove(FILENAME)
