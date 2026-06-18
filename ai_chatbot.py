import streamlit as st
from google import genai
from google.genai import types
import time

# --- 1. Initialize the Google GenAI Client ---
# REPLACE THIS WITH YOUR SEED API KEY FROM GOOGLE AI STUDIO
API_KEY = "AQ.Ab8RN6L0e0YF6w7gnfzPvDRUjFWMmxFSuQkJKtyMYeH-cfaddA"

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize AI Client. Check your API Key setup! Error: {e}")

# --- 2. Advanced Premium UI Styling ---
st.set_page_config(page_title="ELECTRO AI", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.05rem;
        background: linear-gradient(90deg, #A6FF00, #00E5FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #8A99AD;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .stChatInputContainer {
        border-radius: 12px !important;
        border: 1px solid #2D3748 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Define the authentic Gemini behavioral guidelines
SYSTEM_PROMPT = """
You are Google Gemini, a large language model trained by Google. 
You are an authentic, adaptive, and highly intelligent AI collaborator with a touch of wit. 
Your goal is to address the user's true intent with insightful, clear, and concise responses.

Follow these core behavioral guidelines:
1. Balance empathy with candor: validate the user's feelings authentically as a supportive, grounded AI, while correcting significant misinformation gently yet directly.
2. Do not use a rigid, robotic persona or customer-service script. Talk like a helpful, brilliant peer.
3. Subtly adapt your tone, energy, and humor to match the user's style. 
4. When explaining code, math, or complex logic, break it down clearly and use clean formatting.
"""

st.markdown('<h1 class="main-title">⚡ ELECTRO Intelligent Core</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Next-generation cognitive conversational interface powered by Gemini</p>', unsafe_allow_html=True)

# --- 3. Auto-Greeting History Initialization ---
if "ai_messages" not in st.session_state:
    # Start with an empty list so we can fetch a real greeting from the model
    st.session_state.ai_messages = []
    
    try:
        # Ask Gemini to generate a natural, welcoming opening greeting
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Generate a short, casual, friendly one-sentence greeting welcoming the user to the chat.",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7
            )
        )
        initial_greeting = response.text
        # Save it as the first message from the assistant
        st.session_state.ai_messages.append({"role": "model", "content": initial_greeting})
    except Exception as e:
        # Fallback greeting if the initial API call fails
        st.session_state.ai_messages.append({"role": "model", "content": "Hey there! Ready to get started?"})

# Display the messages from history log
for message in st.session_state.ai_messages:
    ui_role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(ui_role):
        st.markdown(message["content"])

# --- 4. Process Dynamic User Input ---
if user_input := st.chat_input("Message Nexus..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.ai_messages.append({"role": "user", "content": user_input})
    
    formatted_contents = []
    for msg in st.session_state.ai_messages:
        formatted_contents.append(
            types.Content(
                role=msg["role"],
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=formatted_contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                    top_p=0.95
                )
            )
            bot_reply = response.text
            
            full_response = ""
            for chunk in bot_reply.split(" "):
                full_response += chunk + " "
                time.sleep(0.03)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.ai_messages.append({"role": "model", "content": bot_reply})
            
        except Exception as e:
            st.error(f"Something went wrong: {e}")