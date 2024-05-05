from flask import Flask, request, jsonify
from flask_cors import CORS
import json

import os
from dotenv import load_dotenv
import google.generativeai as gen_ai
from langdetect import detect
from googletrans import Translator

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Function to detect and translate text to English
def detect_and_translate_to_english(text):
    translator = Translator()
    detected_language = detect(text)
    if detected_language != 'en':
        translated_text = translator.translate(text, src=detected_language, dest='en').text
    else:
        translated_text = text
    return [detected_language, translated_text]


# Function to translate text back to the original detected language
def translate_to_original_language(text, original_language):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest=original_language).text
    return translated_text


app = Flask(__name__)
CORS(app)

@app.route('/translate', methods=['POST'])
def translateEnglish():
    try:
        asJson = json.loads(request.get_data(as_text=True))
        [lang, ans] = detect_and_translate_to_english(asJson['text'])
        print('prompt:', asJson['text'][:15])
        print('detected:', lang)

        return {
            "text": ans,
            "language": lang
        }
    except Exception:
        pass

    return {}

@app.route('/translate/native', methods=['POST'])
def translateNative():
    try:
        asJson = json.loads(request.get_data(as_text=True))
        nativeText = translate_to_original_language(asJson["text"], asJson["language"])

        return {
            "text": nativeText
        }
    except Exception:
        pass

    return {}

if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Run the Flask app on port 8080 in debug mode
