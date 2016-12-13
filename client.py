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
            json={
                "text": text
            }
        ).json()

        print(response)

        if "response" in response:
            to_speak = response["response"]
        else:
            to_speak = "Sorry, I didn't catch that. Try again?"

        print("SAYING:", to_speak)
        speak(to_speak)

except KeyboardInterrupt:
    print("Exiting.")
