import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    print(
        "------------------------------ Please Speak -----------------------------------"
    )
    while True:
        try:
            audio_data = recognizer.listen(source)
            text = recognizer.recognize_google(audio_data)
            print(text)
        except sr.UnknownValueError:
            print("Please Speak Clearly")
