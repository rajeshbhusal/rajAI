from openai import OpenAI
import streamlit as st
import os

st.set_page_config(page_title="Welcome to Raj AI", page_icon="🤘",layout="wide")

# Function to clear the chat history
def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

with st.sidebar:
    # Button to clear the chat history
    openai_api_key = st.text_input("Input your OpenAI API Key", key="chatbot_api_key", type="password")
    if st.button("Clear Chat",use_container_width=True):
        clear_chat()
        st.session_state.clear_message_displayed = True
    # Allow user to upload a file to pass on to ChatGPT
    # uploaded_file = st.file_uploader("Upload a file", type=("txt", "md","pdf","png","jpg"))


st.title("🚀 Raj's Personal Chatbot! 🤘")
st.caption("Powered by OpenAI GPT4o")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

#prompt = st.chat_input()
#if prompt:
if prompt := st.chat_input():
    
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages,stream=True)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        msg = st.write_stream(response)

    st.session_state.messages.append({"role": "assistant", "content": msg})