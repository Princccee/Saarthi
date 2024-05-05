import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from langdetect import detect
from googletrans import Translator

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Bookie!",
    page_icon=":brain:",  # Favicon emoji
    layout="wide",  # Page layout option
)

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
    return translated_text


# Function to translate text back to the original detected language
def translate_to_original_language(text, original_language):
    translator = Translator()
    translated_text = translator.translate(text, src='en', dest=original_language).text
    return translated_text


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🤖 Bookie")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.text_area("Enter your prompt....")  # Allow user to enter text in any Indian regional language
# user_prompt = st.chat_input("Ask Bookie...")

if st.button("Send"):
    if user_prompt:
        # Translate user's prompt to English
        english_prompt = detect_and_translate_to_english(user_prompt)

        # Add translated user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send translated user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(english_prompt)

        # Translate Gemini-Pro's response back to the original detected language
        original_language = detect(user_prompt)
        response_in_original_language = translate_to_original_language(gemini_response.text, original_language)

        # Display Gemini-Pro's response in the original detected language
        with st.chat_message("assistant"):
            st.markdown(response_in_original_language)
