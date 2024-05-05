import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
#from bhashini_api import Bhashini  # Assuming you have a Bhashini API library
from bhashini_translator import Bhashini

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Bookie!",
    page_icon=":brain:",  # Favicon emoji
    layout="wide",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
BHASHINI_API_KEY = os.getenv("BHASHINI_API_KEY")  # Add Bhashini API key

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Display the chatbot's title on the page
st.title("Ask from Bookie")

# Language selection dropdown
source_language = st.selectbox("Choose your language:", ["English", "Hindi", "Tamil", "Telugu","Marathi"])

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Bookie...")
if user_prompt:
    # Add user's message to chat and display it (in source language)
    st.chat_message("user").markdown(user_prompt)

    # Translate user message to English (assuming Gemini-Pro prefers English)
    if source_language != "English":
        bhashini = Bhashini(api_key=BHASHINI_API_KEY)
        try:
            translated_prompt = bhashini.translate(source_language, "en", user_prompt)
        except Exception as e:
            st.error(f"Bhashini translation error: {e}")
            translated_prompt = user_prompt  # Fallback if translation fails

    else:
        translated_prompt = user_prompt

    # Send translated message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(translated_prompt)

    # Translate Gemini-Pro's response back to user's language (if needed)
    if source_language != "English":
        try:
            translated_response = bhashini.translate("en", source_language, gemini_response.text)
        except Exception as e:
            st.error(f"Bhashini translation error: {e}")
            translated_response = gemini_response.text  # Fallback if translation fails
    else:
        translated_response = gemini_response.text

    # Display translated response from Gemini-Pro
    with st.chat_message("assistant"):
        st.markdown(translated_response)