import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz

# ---------- Streamlit Page Settings ----------
st.set_page_config(page_title="EduBot", page_icon="🎓", layout="centered")

# ---------- Session Initialization ----------
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- Load Knowledge Base ----------
@st.cache_data
def load_kb():
    url = "https://docs.google.com/spreadsheets/d/1iuMdndmSVkq8JR6Ir42s29-_3QHcGOX6/export?format=csv"
    df = pd.read_csv(url)
    return dict(zip(df['Question'].str.lower(), df['Answer']))

# ---------- Best Match Logic ----------
def get_best_match(question, kb, threshold=70):
    questions = list(kb.keys())
    match, score, _ = process.extractOne(question.lower(), questions, scorer=fuzz.token_sort_ratio)
    return kb[match] if score >= threshold else "Hmm 🤔 I'm not sure I understand. Could you rephrase?"

# ---------- Welcome Page ----------
def welcome_page():
    st.markdown("### 🎓 Welcome to Yabatech EduBot")
    st.image("assets/yctlogo.jpg", width=100)
    st.subheader("Your Digital Leaning Assistant")
    st.markdown("""
        🚀 **EduBot helps you with:**
        - School admissions and processes  
        - Course guidance and academic support  
        - FAQs about payments, hostels, resumption, etc.  
        
        Just click the button below to start chatting!
    """)
    if st.button("Start Chatbot 💬"):
        st.session_state.page = "chatbot"

# ---------- Chatbot Page ----------
def chatbot_page():
    qa_dict = load_kb()
    st.title("EduBot")
    st.caption("Ask your question below:")

    user_input = st.text_input("You:", key="user_input")

    if user_input:
        if user_input.lower() == "quit":
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", "Goodbye! Stay curious! 👋"))
        else:
            reply = get_best_match(user_input, qa_dict)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", reply))

    # Chat history display
    for speaker, message in st.session_state.chat_history:
        icon = "🧑" if speaker == "You" else ""
        st.markdown(f"{icon} **{speaker}**: {message}")

    if st.button("🔙 Return Home"):
        st.session_state.page = "welcome"

# ---------- Router ----------
if st.session_state.page == "welcome":
    welcome_page()
else:
    chatbot_page()
