import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import os
import webbrowser

engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)


def speak(text):
    print("EDITH:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    listener = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)

    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        print("You:", command)
        return command

    except:
        return ""


speak("Hello Sir. I am EDITH. How can I help you?")


while True:

    command = listen()

    if command == "":
        continue

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "google" in command:
        search = command.replace("google", "")
        speak("Searching Google")
        pywhatkit.search(search)

    elif "play" in command:
        song = command.replace("play", "")
        speak("Playing " + song)
        pywhatkit.playonyt(song)

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak("Current time is " + time)

    elif "date" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak(today)

    elif "who is" in command:
        person = command.replace("who is", "")
        info = wikipedia.summary(person, 2)
        speak(info)

    elif "open notepad" in command:
        os.system("notepad")

    elif "open calculator" in command:
        os.system("calc")

    elif "open chrome" in command:
        chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(chrome)

    elif "shutdown" in command:
        speak("Shutting down computer.")
        os.system("shutdown /s /t 1")

    elif "restart" in command:
        speak("Restarting computer.")
        os.system("shutdown /r /t 1")

    elif "good bye" in command or "exit" in command:
        speak("Goodbye Sir.")
        break

    else:
        speak("I did not understand.")