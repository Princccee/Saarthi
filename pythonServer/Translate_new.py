from langdetect import detect
from googletrans import Translator

translator = Translator()


def detect_and_translate(text):
    # Detect the language
    detected_language = detect(text)

    # If detected language is not English, translate to English
    if detected_language != 'en':
        translated_text = translator.translate(text, src=detected_language, dest='en').text
    else:
        translated_text = text

    return translated_text


def translate_back_to_original(text, original_language):
    # Translate back to the original language
    translated_text = translator.translate(text, src='en', dest=original_language).text

    return translated_text


# Take input from the user
# input_text = input("Enter text in any Indian regional language: ")
# #print(detect(input_text))
#
# # Translate and detect language
# prompt = detect_and_translate(input_text)
# print("Translated to English:", prompt)
#
# original_language = detect(input_text)
# original_text = translate_back_to_original(prompt, original_language)
# print("Translated back to original language:", original_text)