import json

import requests

import config
from swish.recognize import listen, speech_to_text
from swish.speak import speak

try:
    while True:
        print("Begin speaking.")
        speech = listen()
        print("Stopped listening.")

        text = speech_to_text(speech)

        print("YOU SAID:", text)

        response = requests.get(
            config.BASE_URL + "response",
            headers={
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "text": text
            })
        ).json()

        print(response)

        if "response" in response:
            to_speak = response["response"]
        else:
            to_speak = "An error occured."

        print("SAYING:", to_speak)
        speak(to_speak)

        if (input("Continue? [Y/n] ").upper() or 'Y') != 'Y':
            break

except KeyboardInterrupt:
    print("Exiting.")
