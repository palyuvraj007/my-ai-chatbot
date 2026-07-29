import streamlit as st
from google import genai
from google.genai import types
import time

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="ALPHA AI", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. Advanced Premium CSS Styling ---
st.markdown("""
    <style>
    /* Global Reset & Dark Theme */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #161B22 0%, #0D1117 100%);
        color: #E6EDF3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit header/footer noise */
    #MainMenu, header, footer {visibility: hidden;}

    /* Hero Header */
    .header-container {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(166, 255, 0, 0.1);
        border: 1px solid rgba(166, 255, 0, 0.3);
        color: #A6FF00;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #A6FF00;
        border-radius: 50%;
        box-shadow: 0 0 8px #A6FF00;
    }

    .main-title {
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -0.05rem;
        background: linear-gradient(135deg, #FFFFFF 30%, #A6FF00 70%, #00E5FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.1;
    }

    .subtitle {
        color: #8B949E;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Glassmorphism Input Box */
    .stChatInputContainer {
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(22, 27, 34, 0.75) !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #00E5FF !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
    }

    /* Chat Messages Enhancements */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 1rem 0;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0D1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #21262D;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #30363D;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Initialize API & Prompts ---
API_KEY = "YOUR_ACTUAL_API_KEY_HERE"

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize AI Client: {e}")

SYSTEM_PROMPT = """
You are Google Gemini, a large language model trained by Google. 
You are an authentic, adaptive, and highly intelligent AI collaborator with a touch of wit. 
Your goal is to address the user's true intent with insightful, clear, and concise responses.
"""

# --- 4. Render Header UI ---
st.markdown("""
    <div class="header-container">
        <div class="status-badge">
            <span class="pulse-dot"></span> Core Online
        </div>
        <h1 class="main-title">Nexus AI</h1>
        <p class="subtitle">Next-generation cognitive conversational interface powered by Gemini</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. Auto-Greeting & Session State ---
if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Generate a short, casual, friendly one-sentence greeting welcoming the user to the chat.",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7
            )
        )
        initial_greeting = response.text
        st.session_state.ai_messages.append({"role": "model", "content": initial_greeting})
    except Exception:
        st.session_state.ai_messages.append({"role": "model", "content": "System online. How can I assist you today?"})

# --- 6. Render Chat Logs with Icons ---
for message in st.session_state.ai_messages:
    is_assistant = message["role"] == "model"
    avatar = "⚡" if is_assistant else "👤"
    ui_role = "assistant" if is_assistant else "user"
    
    with st.chat_message(ui_role, avatar=avatar):
        st.markdown(message["content"])

# --- 7. Handle User Input ---
if user_input := st.chat_input("Ask Nexus anything..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    st.session_state.ai_messages.append({"role": "user", "content": user_input})
    
    formatted_contents = [
        types.Content(role=msg["role"], parts=[types.Part.from_text(text=msg["content"])])
        for msg in st.session_state.ai_messages
    ]
    
    with st.chat_message("assistant", avatar="⚡"):
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
            
            # Word-by-word streaming effect
            full_response = ""
            for chunk in bot_reply.split(" "):
                full_response += chunk + " "
                time.sleep(0.025)
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.ai_messages.append({"role": "model", "content": bot_reply})
            
        except Exception as e:
            st.error(f"Error generating response: {e}")
        
