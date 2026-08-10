import pyttsx3
import pywhatkit
import wikipedia
import webbrowser
import datetime
import os
import requests

engine = pyttsx3.init()
engine.setProperty("rate", 170)

voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)


def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()


def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")


def get_date():
    return datetime.datetime.now().strftime("%d %B %Y")


def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=3"
        return requests.get(url, timeout=5).text
    except:
        return "Unable to get weather."


speak("Hello! I am Jarvis.")
speak("Type your commands below.")

while True:

    command = input("\nYou: ").lower().strip()

    if command == "":
        continue

    if command == "exit":
        speak("Goodbye!")
        break

    elif "time" in command:
        speak(f"The time is {get_time()}")

    elif "date" in command:
        speak(f"Today is {get_date()}")

    elif command.startswith("google "):
        search = command.replace("google ", "")
        speak("Searching Google")
        pywhatkit.search(search)

    elif command.startswith("youtube"):
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif command.startswith("play "):
        song = command.replace("play ", "")
        speak(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif command.startswith("who is "):
        person = command.replace("who is ", "")
        try:
            info = wikipedia.summary(person, sentences=2)
            speak(info)
        except:
            speak("I couldn't find information.")

    elif command.startswith("weather "):
        city = command.replace("weather ", "")
        speak(get_weather(city))

    elif command == "open notepad":
        os.system("notepad")

    elif command == "open calculator":
        os.system("calc")

    elif command == "open paint":
        os.system("mspaint")

    elif command == "open cmd":
        os.system("start cmd")

    elif command == "open chrome":
        chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if os.path.exists(chrome):
            os.startfile(chrome)
        else:
            speak("Chrome not found.")

    elif command == "shutdown":
        speak("Shutting down.")
        os.system("shutdown /s /t 5")

    elif command == "restart":
        speak("Restarting.")
        os.system("shutdown /r /t 5")

    elif command == "sleep":
        speak("Going to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    else:
        speak("Sorry, I don't understand that command.")

    