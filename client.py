from swish.recognize import get_result_response, listen, speech_to_text
from swish.speak import speak

try:
    while True:
        print("Begin speaking.")
        speech = listen()
        print("Stopped listening.")

        text = speech_to_text(speech)

        print("YOU SAID:", text)

        for response in get_result_response(text):
            print("SAYING:", response)
            speak(response)

        if (input("Continue? [Y/n] ").upper() or 'Y') != 'Y':
            break

except KeyboardInterrupt:
    print("Exiting.")
