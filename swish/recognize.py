import speech_recognition as sr

from .parse import parse_intent

recognizer = sr.Recognizer()


def speech_to_text(source, recognizer=recognizer):
    try:
        return recognizer.recognize_google(source)
    except sr.UnknownValueError:
        return None
    except Exception:
        return False


def respond_to_parsed(result):
    for intent in parse_intent(result):
        if intent.get("confidence") > 0:

            number = intent.get("PlasticNumber")

            if number is None:
                yield "I'm not sure what kind of plastic that is."
            elif number == "6":
                yield "Number 6 plastic is not recyclable."
            else:
                yield "Number {0} plastic is recyclable!".format(number)


def get_result_response(result):
    if result is False:
        yield "Sorry, something went wrong."
    elif result is None:
        yield "Sorry, I'm not sure what you said."
    else:
        yield from respond_to_parsed(result)


def listen():
    with sr.Microphone() as source:
        return recognizer.listen(source)


if __name__ == '__main__':
    print(speech_to_text(listen()))
