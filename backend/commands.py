import pyttsx3
import speech_recognition as sr
import eel
import time
from backend.helper import extract_weather_query


def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()


@eel.expose
def takeCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    
    return query.lower()


@eel.expose
def allCommands():
    query = takeCommand()

    try:
        if "open" in query:
            from backend.feature import openCommand
            openCommand(query)

        elif extract_weather_query(query):
            from backend.feature import get_weather
            speak("Which city are you asking about?")
            eel.DisplayMessage("Which city are you asking about?")
            city = takeCommand()
            
            if city:
                weather_info = get_weather(city)
                speak(weather_info)
                eel.DisplayMessage(weather_info)
            else:
                speak("I didn't catch the city name.")
                eel.DisplayMessage("I didn't catch the city name.")
                
        elif "on youtube" in query:
            from backend.feature import playYoutube
            playYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from backend.feature import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takeCommand()
                    
                elif "phone call" in query:
                    flag = 'phone call'
                else:
                    flag = 'video call'
                    
                whatsApp(contact_no, query, flag, name)

        else:
            print("chatbot")
            from backend.feature import ChatBot
            ChatBot(query)

    except Exception as e:
        print("error: ", e)
        
    eel.ShowHood()


@eel.expose
def allChatCommands(query):
    try:
        if "open" in query:
            from backend.feature import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from backend.feature import playYoutube
            playYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from backend.feature import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    message = 'message'
                    speak("what message to send")
                    query = takeCommand()
                    
                elif "phone call" in query:
                    message = 'phone call'
                else:
                    message = 'video call'
                    
                whatsApp(contact_no, query, message, name)

        else:
            print("chatbot")
            from backend.helper import Chatting
            Chatting(query)
    except:
        print("error")