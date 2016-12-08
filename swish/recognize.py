import speech_recognition as sr

recognizer = sr.Recognizer()


def speech_to_text(source, recognizer=recognizer):
    try:
        return recognizer.recognize_google(source)
    except Exception:
        return ""


def listen():
    with sr.Microphone() as source:
        return recognizer.listen(source)


if __name__ == '__main__':
    print(speech_to_text(listen()))
