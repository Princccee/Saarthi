import streamlit as st
from langdetect import detect
from googletrans import Translator

translator = Translator()


def detect_and_translate(text, target_language):
    # Detect the language
    detected_language = detect(text)

    # Translate to the target language
    if detected_language != target_language:  # If already in the target language, no need to translate
        translated_text = translator.translate(text, src=detected_language, dest=target_language).text
    else:
        translated_text = text

    return translated_text


# Streamlit web app
def main():
    st.title("Language Translation")

    # Input field for user's message
    user_input = st.text_area("Enter text to translate:")

    # Dropdown for selecting target language
    target_language = st.selectbox("Select target language:", ["English", "Hindi", "Tamil", "Telugu"])

    # Map target languages to language codes used by Google Translate
    language_codes = {"English": "en", "Hindi": "hi", "Tamil": "ta", "Telugu": "te"}

    if st.button("Translate"):
        # Convert target language to language code used by Google Translate
        target_language_code = language_codes[target_language]

        # Translate the input text
        translated_text = detect_and_translate(user_input, target_language_code)

        # Display translated text
        st.write("Translated Text:", translated_text)


if __name__ == "__main__":
    main()
