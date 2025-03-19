import os
from pipes import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
import requests
from playsound import playsound
import eel
import pyaudio
import pyautogui
import pywhatkit as kit
import pvporcupine
from backend.commands import speak
from backend.helper import extract_yt_term, remove_words
from backend.config import ASSISTANT_NAME


@eel.expose
def playAssistantSound(file):
    playsound(file)


def openCommand(query):
    from backend.commands import speak
    con = sqlite3.connect("niels.db")
    cursor = con.cursor()
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()
    print(f"App name extracted: {query}")

    if query:
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (query,))
            results = cursor.fetchall()

            if results:
                speak(f"Opening {query}")
                os.startfile(results[0][0])
                return


            cursor.execute('SELECT url FROM web_command WHERE name = ?', (query,))
            results = cursor.fetchall()
            
            if results:
                speak(f"Opening {query}")
                webbrowser.open(results[0][0])
                return

            speak(f"Opening {query}")
            os.system(query)

        except Exception as e:
            speak("Something went wrong")
            print("Error:", e)


def playYoutube(query):
    from backend.commands import speak
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine = None
    paud = None
    audio_stream = None

    try:
        ''' Get the Access key for the Suitable hotword you choose from (https://picovoice.ai/platform/porcupine/)
        1> Sign in to the website and create a hotword
        2> Download the .ppn file into the project folder
        3> Copy the Access key displayed in the screen
        '''
        porcupine = pvporcupine.create(
            access_key="YOUR_ACCESS_KEY",
            keyword_paths=["YOUR_HOTWORD_FILE_IN_PPN_FORMAT_PATH"] # Save the ppn document in the project folder and provide its path
        )

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for 'neils'...")

        while True:
            keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("Hotword detected!")

                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("o")
                time.sleep(2)
                autogui.keyUp("win")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


def get_weather(city):
    API_KEY = "YOUR_API_KEY"    # Get api key form (https://openweathermap.org/)
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(URL)
        data = response.json()

        if data["cod"] == 200:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            weather_report = f"The weather in {city} is {weather_desc} with a temperature of {temp}°C and humidity of {humidity}%."
            return weather_report
        else:
            return "Sorry, I couldn't fetch the weather information right now. Please check the city name."
    except Exception as e:
        return "Error retrieving weather data."


def findContact(query):
    con = sqlite3.connect("neils.db")
    cursor = con.cursor()
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    from backend.commands import speak

    if flag == 'message':
        target_tab = 20
        neils_message = "message send successfully to "+name

    elif flag == 'phone call':
        target_tab = 15
        message = ''
        neils_message = "calling to "+name

    else:
        target_tab = 13
        message = ''
        neils_message = "staring video call with "+name

    encoded_message = quote(message)

    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    full_command = f'start "" "{whatsapp_url}"'

    subprocess.run(full_command, shell=True)
    time.sleep(10)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(neils_message)


import json
import requests
from backend.commands import speak

def ChatBot(query):
    API_URL = "https://api.cohere.ai/v1/generate"
    API_KEY = "YOUR_API_KEY"    # Get API key form Cohere

    system_prompt = (
        "You are NIELS, an AI virtual assistant. "
        "Be helpful, polite, and friendly. "
        "Answer only for what i ask, Give response in one line."
    )

    user_input = query + system_prompt

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "prompt": user_input,
            "max_tokens": 100,
            "temperature": 0.5,
            "k": 0,
            "p": 0.75,
            "stop_sequences": ["\n"],
            "return_likelihoods": "NONE"
        }
    )

    if response.status_code == 200:
        bot_response = response.json().get("generations", [{}])[0].get("text", "").strip()
    else:
        print(f"Error from Cohere: {response.text}")
        bot_response = f"Sorry, I couldn't process your request. Error: {response.text}"

    json_file_path = "frontend/chatbot_responses.json"
    chat_data = {"user": query, "bot": bot_response}

    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = []
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(chat_data)

    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=4)

    speak(bot_response)
    print(bot_response)

    return bot_response


