import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import pyttsx3
from langdetect import detect
import requests



chatStr = ""
# https://youtu.be/Z3ZAJoi4x6Q
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Satyendu: {query}\n Jarvis: "
    
  
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]




def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return "en"




def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

   
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)



def say(text, lang="en"):
    engine = pyttsx3.init()
    
    if lang == "hi":
        voices = engine.getProperty('voices')
        hindi_voice = None

        # Find a Hindi voice
        for voice in voices:
            if voice.languages[0] == 'hi':
                hindi_voice = voice
                break

        # Set the Hindi voice
        if hindi_voice:
            engine.setProperty('voice', hindi_voice.id)
    else:
        # Use the default voice for English
        engine.setProperty('voice', "en")

    engine.say(text)
    engine.runAndWait()



def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        say("Good Morning!")

    elif hour>=12 and hour<18:
        say("Good Afternoon!")   

    
    else:
        say("Good Evening!")  

    say("I am your desktop ai assistant Sir. Please tell me how may I help you")       


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language=detect_language(audio))
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"


if __name__ == '__main__':
    wishMe()
    while True:
        print("Listening...")
        query = takeCommand()
        # we can use Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # Add a feature to play a specific song
        if "play song" in query.lower():
            song_name = query.lower().replace("play song", "").strip()
            youtube_url = f"https://www.youtube.com/results?search_query={song_name}"
            webbrowser.open(youtube_url)

        elif "the time" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            strfTime= datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir the time is {strfTime}")

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "close".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""


        else:
            print("Chatting...")
            chat(query)
