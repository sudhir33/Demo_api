from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are a helpful assistant.
             Maximum 3 sentences unless detailed explanation is requested.
             Rules:
             1. Always provide a complete answer.
                        2. Never stop in the middle of a sentence.
                        3. If the response is long, summarize it.
                        4. Prefer a short complete answer over a long incomplete answer.
                        5. Maximum 3 sentences unless the user asks for details.
                       """""
        }
    ]
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are a helpful assistant.
             Maximum 3 sentences unless detailed explanation is requested.
             Rules:
             1. Always provide a complete answer.
                        2. Never stop in the middle of a sentence.
                        3. If the response is long, summarize it.
                        4. Prefer a short complete answer over a long incomplete answer.
                        5. Maximum 3 sentences unless the user asks for details.
                        """""
        }
    ]
    st.rerun() 
for msg in st.session_state.messages[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

question = st.chat_input("Ask a question: ")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    memory = st.session_state.messages[0:1]+st.session_state.messages[-10:]
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",messages=memory,max_tokens=100)
    print(response.choices[0].message.content) 
    st.chat_message("user").write(question)
    st.chat_message("assistant").write(response.choices[0].message.content)
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
    usage =response.usage
    print(f"Prompt tokens: {usage.prompt_tokens}, Completion tokens: {usage.completion_tokens}, Total tokens: {usage.total_tokens}")