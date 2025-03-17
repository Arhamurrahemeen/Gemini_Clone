import streamlit as st
import google.generativeai as genai
import json
import os

# Configure Gemini API
genai.configure(api_key="AIzaSyAicOVimMvQevQy5oKBbyZ3-4ywK7IHnk8")

st.title("Gemini Chatbot")

HISTORY_FILE = "chat_history.json"

# Function to load chat history
def load_chat_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save chat history
def save_chat_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file)

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# 🔹 FILE UPLOAD - Now placed at the top
st.sidebar.header("Upload a File")
uploaded_file = st.sidebar.file_uploader("Upload PDF, TXT, or Image", type=["pdf", "txt", "png", "jpg", "jpeg"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

    # Handle text files separately
    if uploaded_file.type == "text/plain":
        file_content = file_bytes.decode("utf-8")
        st.sidebar.text_area("File Preview", file_content, height=150)

    else:
        file_content = "Uploaded file is not text-based."

    st.session_state.messages.append({"role": "user", "content": f"Uploaded: {uploaded_file.name}"})
    model = genai.GenerativeModel("gemini-2.0-pro-vision")  
    response = model.generate_content(file_content)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    save_chat_history(st.session_state.messages)

# 🔹 DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 🔹 CHAT INPUT
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    save_chat_history(st.session_state.messages)

# 🔹 CLEAR CHAT HISTORY BUTTON
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    save_chat_history([])
    st.rerun()
