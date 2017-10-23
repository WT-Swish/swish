import speech_recognition as sr


def speech_to_text(source, recognizer):
    try:
        return recognizer.recognize_google(source)
    except Exception:
        return ""


def listen(callback, recognizer, microphone):

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    return recognizer.listen_in_background(microphone, callback)

if __name__ == '__main__':

    import time

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    stop_listen = listen(
        lambda r, m: print(speech_to_text(m, recognizer=r)),
        recognizer, microphone
    )
    print("Listening...")

    time.sleep(5)

    stop_listen()
    print("Stopped listening.")
