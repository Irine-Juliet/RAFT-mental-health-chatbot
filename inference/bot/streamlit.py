# LOCAL - app.py
import streamlit as st
import requests

API_URL = "https://b3c7-34-19-11-117.ngrok-free.app"  # Copy the URL printed in Colab

st.set_page_config(page_title="Mental Health Support")

with st.sidebar:
    st.title('Mental Health Support Chatbot')

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there! How can I help you today?"}]

def get_bot_response(question):
    response = requests.post(
        f"{API_URL}/generate",
        json={
            "question": question,
            "conversation_history": st.session_state.messages
        }
    )
    return response.json()["response"]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input and response
if prompt := st.chat_input():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_bot_response(prompt)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})