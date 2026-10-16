
import streamlit as st
import sys
from importlib import import_module
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage

sys.path.insert(0, str(Path(__file__).resolve().parent))
ask_agent = import_module("main").ask_agent

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎",
    layout="centered",
)

st.title("Research Agent")
st.caption("An AI assistant that can search the web and synthesize findings.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("About")
    st.write(
        "This agent uses an LLM and a Tavily web-search tool "
        "to research questions and summarize findings."
    )

    if st.button("Clear conversation"):
        st.session_state.chat_history = []
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a research question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            try:
                answer = ask_agent(
                    question,
                    st.session_state.chat_history,
                )
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")
