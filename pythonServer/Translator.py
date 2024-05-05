from langdetect import detect
from googletrans import Translator


def translate_to_english(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='en').text
    return translated_text


def translate_to_detected_language(text):
    detected_language = detect(text)
    translator = Translator()
    translated_text = translator.translate(text, dest=detected_language).text
    return translated_text


def main():
    print("Welcome to the Language Translator!")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("\nEnter text to translate: ")
        if user_input.lower() == 'quit':
            print("Exiting...")
            break

        try:
            detected_language = detect(user_input)
            print(f"Detected language: {detected_language}")

            english_translation = translate_to_english(user_input)
            print(f"English translation: {english_translation}")

            original_language_translation = translate_to_detected_language(english_translation)
            print(f"Translation back to detected language: {original_language_translation}")
        except Exception as e:
            print("Error occurred:", e)


if __name__ == "__main__":
    main()
