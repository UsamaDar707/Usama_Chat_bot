import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO  # Import BytesIO
import base64

# Import your Gemini API key
api_key = st.secrets["gemini_api_key"]
#api_key = "AIzaSyC7zYuESCXYAiFcu4LVwYLrey2tNppZbG0"
genai.configure(api_key=api_key )

# Initialize the model
model = genai.GenerativeModel('gemini-pro')

# Load and encode the logo image
logo_path = "Chatbot Logo.jpg"
logo_image = Image.open(logo_path)
buffered = BytesIO()
logo_image.save(buffered, format="JPEG")
encoded_logo = base64.b64encode(buffered.getvalue()).decode()

# Streamlit interface with logo and header
st.markdown(f"""
    <style>
    .header {{
        background: linear-gradient(to right, #007bff, #00c6ff);
        padding: 20px;
        text-align: center;
        color: white;
        font-size: 24px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .header img {{
        margin-right: 10px;
    }}
    </style>
    <div class="header">
        <img src="data:image/jpg;base64,{encoded_logo}" width="50"/>
        <span>😎 Usama_Dar Interactive Chat-Bot 😎</span>
    </div>
""", unsafe_allow_html=True)

st.write("Powered by Usama_Dar")
st.write("For Help email: usamadar707@gmail.com")

# Custom CSS for layout adjustments
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f9f9f9;
        margin: 0;
        padding: 0;
    }
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 15px;
        background: linear-gradient(to bottom, #ffffff, #e0e0e0);
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        margin-bottom: 70px; /* Add margin to keep space for input form */
        border: 1px solid #ccc;
    }
    .user-message, .bot-message {
        border-radius: 15px;
        padding: 12px;
        margin: 8px 0;
        max-width: 75%;
    }
    .user-message {
        background-color: #007bff;
        color: white;
        align-self: flex-end;
    }
    .bot-message {
        background-color: #28a745;
        color: white;
        align-self: flex-start;
    }
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #ffffff;
        padding: 10px 20px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1; /* Ensure it is on top of chat */
        border-top: 1px solid #ddd;
    }
    .stTextInput {
        width: 75%;
        border-radius: 20px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .stButton button {
        width: 20%;
        border-radius: 20px;
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# Function to get response from the model
def response(get_input):
    previous_context = ""
    if st.session_state.history:
        previous_context = "Conversation history:\n" + "\n".join(
            [f"User: {user_msg}\nBot: {bot_msg}" for user_msg, bot_msg in st.session_state.history]
        ) + "\n\n"
    
    full_prompt = previous_context + f"User: {get_input}\nBot:"
    Model_response = model.generate_content(full_prompt)
    return Model_response.text.strip()

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Input form at the bottom (footer position)
with st.form(key="Chat", clear_on_submit=True):
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    user_input = st.text_input("", key="user_input")
    submit_button = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

    if submit_button:
        if user_input:
            output = response(user_input)
            st.session_state.history.insert(0, (user_input, output))  # Add new messages to the top
        else:
            st.warning("Enter the Prompt")

# Chat history container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for user_message, bot_message in st.session_state.history:
    st.markdown(f'<div class="user-message">{user_message}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-message">{bot_message}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
