import requests
import speech_recognition as sr

import config
from swish.recognize import listen, speech_to_text
from swish.speak import speak


def callback(recognizer, audio):

    text = speech_to_text(audio, recognizer)

    print("[HEARD]:", text)

    response = requests.get(
        config.BASE_URL + "response",
        json={
            "text": text
        }
    ).json()

    print(response)

    if "response" in response:
        to_speak = response["response"]
    else:
        to_speak = "Sorry, I didn't catch that. Try again?"

    print("[SAYING]:", to_speak)
    speak(to_speak)


def run(before_start, before_stop):

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:

        before_start()

        print("Listening...")
        stop_listen = listen(callback, recognizer, microphone)

        before_stop()

        print("Stopped listening.")
        stop_listen()


if __name__ == "__main__":

    import time

    def before_start():
        input()

    def before_stop():
        time.sleep(5)

    try:
        run(before_start, before_stop)
    except KeyboardInterrupt:
        print("Exiting.")
