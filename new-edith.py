"""
EDITH - A simple Python voice assistant
----------------------------------------
Listens to your voice, speaks back, executes commands,
types dictated text into whatever window is focused,
and tells jokes.

SETUP (run once in a terminal):
    pip install -r requirements.txt

    Windows users may also need:
        pip install pipwin
        pipwin install pyaudio

    Mac users may need:
        brew install portaudio
        pip install pyaudio

RUN:
    python edith.py

HOW IT WORKS:
    - Say "Edith" (the wake word) then wait for the beep-like pause,
      then say your command. Or just talk continuously — see USE_WAKE_WORD below.
    - Say "type <something>" and it will type that text into
      whatever application/window currently has focus (Notepad,
      browser, chat box, etc.) — e.g. "type pej one two three"
      will type "pej one two three" (numbers spoken as words get
      converted to digits automatically for short alphanumeric codes).
    - Say "tell me a joke" for a joke.
    - Say "stop" or "exit" or "goodbye" to quit.
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import random
import os
import sys
import time

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

# ----------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------
WAKE_WORD = "edith"
USE_WAKE_WORD = False   # Set True if you want to say "Edith" before every command
ASSISTANT_NAME = "Edith"

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the computer go to therapy? It had too many unresolved issues.",
    "I would tell you a UDP joke, but you might not get it.",
    "There are 10 types of people in the world: those who understand binary, and those who don't.",
    "Why do Java developers wear glasses? Because they don't see sharp.",
    "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
    "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
    "I told my computer I needed a break, and now it won't stop sending me KitKats.",
    "Why do programmers hate nature? It has too many bugs and no debugger.",
    "What do you call a programmer from Finland? Nerdic.",
]

# ----------------------------------------------------------------------
# INIT ENGINES
# ----------------------------------------------------------------------
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 175)

# Try to pick a pleasant voice if available
voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)


def speak(text: str):
    """Speak text out loud and also print it."""
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()


def listen(timeout=5, phrase_time_limit=8):
    """Listen from the microphone and return recognized text (lowercase) or ''."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("My speech service seems to be unavailable right now. Check your internet connection.")
        return ""


# ----------------------------------------------------------------------
# HELPER: convert spoken words into a typed code, e.g. "pej one two three" -> "pej123"
# ----------------------------------------------------------------------
NUMBER_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "oh": "0",
}


def words_to_code(spoken: str) -> str:
    """
    Turns something like 'pej one two three' into 'pej123'.
    Any recognized number-word becomes a digit; everything else
    is glued together with no spaces, useful for codes/usernames/passwords.
    Also handles it if you just say the code normally, e.g. 'pej123'.
    """
    parts = spoken.split()
    out = []
    for word in parts:
        if word in NUMBER_WORDS:
            out.append(NUMBER_WORDS[word])
        else:
            out.append(word)
    return "".join(out)


def type_text(raw_text: str):
    """Types text into whatever window currently has focus."""
    if not HAS_PYAUTOGUI:
        speak("I need the pyautogui library installed to type text for you. Please run: pip install pyautogui")
        return

    code = words_to_code(raw_text)
    speak(f"Typing {raw_text} now. Click into the window you want it typed into.")
    time.sleep(2)  # gives you time to click into the target window
    pyautogui.write(code, interval=0.05)
    speak("Done.")


# ----------------------------------------------------------------------
# COMMAND HANDLING
# ----------------------------------------------------------------------
def handle_command(command: str) -> bool:
    """
    Executes a single command.
    Returns False if the assistant should stop, True to keep listening.
    """
    if not command:
        return True

    if any(word in command for word in ["stop", "exit", "quit", "goodbye", "shut down"]):
        speak("Goodbye. Shutting down.")
        return False

    if "joke" in command:
        speak(random.choice(JOKES))

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"It's {now} right now.")

    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}.")

    elif command.startswith("search for") or command.startswith("google"):
        query = command.replace("search for", "").replace("google", "").strip()
        if query:
            speak(f"Searching for {query}.")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What should I search for?")

    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")

    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://google.com")

    elif command.startswith("open "):
        # generic: "open <website or app name>"
        target = command.replace("open", "", 1).strip()
        if target:
            speak(f"Opening {target}.")
            # If it looks like a website, open in browser, else try as an app
            if "." in target or target in ("gmail", "whatsapp", "spotify", "github"):
                url = target if target.startswith("http") else f"https://{target}.com"
                webbrowser.open(url)
            else:
                try:
                    os.startfile(target)  # Windows only
                except Exception:
                    speak(f"I couldn't find an application called {target} on this system.")

    elif command.startswith("type "):
        # e.g. "type pej one two three" -> types "pej123"
        text_to_type = command.replace("type", "", 1).strip()
        type_text(text_to_type)

    elif "your name" in command:
        speak(f"I'm {ASSISTANT_NAME}, your personal assistant.")

    elif "how are you" in command:
        speak("I'm running perfectly, thanks for asking!")

    else:
        speak("I heard you, but I don't have a command set up for that yet.")

    return True


# ----------------------------------------------------------------------
# MAIN LOOP
# ----------------------------------------------------------------------
def main():
    speak(f"{ASSISTANT_NAME} online. How can I help you?")

    running = True
    while running:
        if USE_WAKE_WORD:
            heard = listen(timeout=None, phrase_time_limit=4)
            if WAKE_WORD not in heard:
                continue
            speak("Yes?")
            command = listen()
        else:
            command = listen()

        running = handle_command(command)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Goodbye.")
        sys.exit(0)