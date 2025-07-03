import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import pywhatkit
import wikipedia
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
engine = pyttsx3.init()

# Basic configuration for the assistant
def configure_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # 1 for female, 0 for male
    engine.setProperty('rate', 150)  # Speaking speed

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()
    return text  # Return for web interface

def take_command():
    """Listen for voice commands"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        print("Say that again please...")
        return "None"

def process_command(query):
    """Process the recognized command"""
    response = ""
    
    if 'time' in query:
        time = datetime.datetime.now().strftime("%I:%M %p")
        response = speak(f"The current time is {time}")
        
    elif 'date' in query:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        response = speak(f"Today's date is {date}")
        
    elif 'search' in query:
        query = query.replace("search", "")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        response = speak(f"Searching for {query}")
        
    elif 'youtube' in query:
        query = query.replace("play on youtube", "")
        pywhatkit.playonyt(query)
        response = speak(f"Playing {query} on YouTube")
        
    elif 'wikipedia' in query:
        query = query.replace("wikipedia", "")
        info = wikipedia.summary(query, sentences=2)
        response = speak(f"According to Wikipedia: {info}")
        
    elif 'open code' in query:
        code_path = "C:\\Users\\Username\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(code_path)
        response = speak("Opening Visual Studio Code")
        
    elif 'shutdown' in query:
        response = speak("Goodbye!")
        os._exit(0)
        
    else:
        response = speak("I didn't understand that. Can you please repeat?")
    
    return response

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/voice', methods=['POST'])
def voice_command():
    try:
        query = take_command()
        response = process_command(query)
        return jsonify({'query': query, 'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    configure_voice()
    app.run(debug=True)
