import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
genai.configure(api_key=GOOGLE_API_KEY)

# Load gemini-1.5 Flash vision model
def gemini_1_5_flash():
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

# get response from gemini pro vision model
def gemini_vision_response(model, prompt, image):
    response = model.generate_content([prompt, image])
    return response.text

# Set page title and icon
st.set_page_config(
    page_title="Medical Chatbot",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    user_picked = option_menu(
        "Google Gemini AI",
        ["ChatBot", "Image Captioning"],
        menu_icon="robot",
        icons = ["chat-dots-fill", "image-fill"],
        default_index=0
    )

def roleForStreamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role
    
if user_picked == 'ChatBot':
    model = gemini_1_5_flash()
    
    if "chat_history" not in st.session_state:
        st.session_state['chat_history'] = model.start_chat(history=[])

    st.title("🤖TalkBot")

    #Display the chat history
    for message in st.session_state.chat_history.history:
        with st.chat_message(roleForStreamlit(message.role)):    
            st.markdown(message.parts[0].text)

    # Get user input
    user_input = st.chat_input("Message TalkBot:")
    if user_input:
        st.chat_message("user").markdown(user_input)
        reponse = st.session_state.chat_history.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(reponse.text)


if user_picked == 'Image Captioning':
    model = gemini_1_5_flash()

    st.title("🖼️Image Input")

    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    user_prompt = """Describe the provided medical image
                    in such a manner as if you are an experienced medical professional with
                    many years of experience. Also try to have a compassionate chat with the user
                    as he/she might have contracted an illness described in the image."""

    if st.button("Generate Caption"):
        load_image = Image.open(image)

        colLeft, colRight = st.columns(2)

        with colLeft:
            st.image(load_image.resize((800, 500)))

        caption_response = gemini_vision_response(model, user_prompt, load_image)

        with colRight:
            st.info(caption_response)


