import re
import eel


def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)  
    return match.group(1) if match else None


def remove_words(input_string, words_to_remove):
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    result_string = ' '.join(filtered_words)

    return result_string


def extract_weather_query(query):
    weather_patterns = [
        r"\bweather today\b",
        r"\bcurrent weather\b",
        r"\bwhat's the weather like\b",
        r"\bhow's the weather\b",
        r"\bhow's the weather today\b"
    ]
    
    for pattern in weather_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return True
    return False


@eel.expose
def chatDisplay(query):
    eel.DisplayMessage(query)


def Chatting(query):
    import json
    import requests

    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    API_KEY = "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"

    identity_questions = [
        "what is your name", "what's your name", "who are you", "what do they call you",
        "tell me your name", "may I know your name", "what should I call you",
        "introduce yourself", "who am I talking to", "yo, what's your name?",
        "hey, who are you?", "what do I call you?", "who dis?"
    ]

    system_prompt = (
        "Be helpful, polite, and friendly. "
        "Answer only for what I ask."
    )

    if query.lower() in identity_questions:
        system_prompt = (
        "Your name is NEILS, an AI virtual assistant and a prototype version designed for higher-end devices. "
        "Be helpful, polite, and friendly. "
        "Answer only for what I ask."
        )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mixtral-8x7b-32768",
            "messages": messages,
            "max_tokens": 100,
            "temperature": 0.5,
            "n": 1,
            "stop": ["\n"]
        }
    )

    if response.status_code == 200:
        bot_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    else:
        print(f"Error from Groq: {response.text}")
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

    print(bot_response)
    return bot_response

