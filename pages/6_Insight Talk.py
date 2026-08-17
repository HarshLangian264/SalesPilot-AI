"""
AI Assistant Page

Conversational AI interface for interacting with
the uploaded dataset.
"""

import streamlit as st

from src.chatbot import ChatBot


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AI Assistant | SalesPilot AI",
    page_icon="🤖",
    layout="wide"
)


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🤖 AI Sales Assistant")

st.caption(
    "Ask questions about your dataset, analyze trends, "
    "generate forecasts, and get AI-powered insights."
)


# ==========================================================
# CHECK DATASET
# ==========================================================

if "clean_df" not in st.session_state:

    st.warning(
        "Please upload and process a dataset first."
    )

    st.stop()


df = st.session_state["clean_df"]


if df is None or df.empty:

    st.warning(
        "The current dataset is empty."
    )

    st.stop()


# ==========================================================
# INITIALIZE / RE-INITIALIZE CHATBOT
# ==========================================================

if (
    "chatbot" not in st.session_state 
    or st.session_state["chatbot"] is None
    or st.session_state["chatbot"].df is not df
):
    st.session_state["chatbot"] = ChatBot(dataframe=df)
    st.session_state["chat_history"] = []

chatbot = st.session_state["chatbot"]


# ==========================================================
# RESET CHAT HISTORY INITIALIZATION
# ==========================================================

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []



# ==========================================================
# SUGGESTED QUESTIONS
# ==========================================================

st.subheader("💡 Try asking")

suggestions = [
    "Give me a summary of this dataset",
    "What are the main trends in the data?",
    "Which areas are performing best?",
    "Forecast the next 6 months",
]


cols = st.columns(4)


for i, suggestion in enumerate(suggestions):

    with cols[i]:

        if st.button(
            suggestion,
            use_container_width=True
        ):

            st.session_state[
                "pending_question"
            ] = suggestion


# ==========================================================
# DISPLAY CHAT HISTORY
# ==========================================================

for message in st.session_state["chat_history"]:

    role = message["role"]

    content = message["content"]

    with st.chat_message(role):

        st.markdown(content)


# ==========================================================
# CHAT INPUT
# ==========================================================

question = st.chat_input(
    "Ask something about your data..."
)


# ==========================================================
# HANDLE SUGGESTED QUESTION
# ==========================================================

if (
    "pending_question" in st.session_state
    and st.session_state["pending_question"]
):

    question = st.session_state.pop(
        "pending_question"
    )


# ==========================================================
# PROCESS QUESTION
# ==========================================================

if question:

    # ----------------------------------------------
    # User message
    # ----------------------------------------------

    st.session_state["chat_history"].append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)


    # ----------------------------------------------
    # AI response
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing your data..."
        ):

            try:

                response = chatbot.chat(
                    question
                )

                st.markdown(response)

            except Exception as e:

                response = (
                    "I couldn't process that request. "
                    f"Error: {e}"
                )

                st.error(response)


    # ----------------------------------------------
    # Save AI response
    # ----------------------------------------------

    st.session_state["chat_history"].append(
        {
            "role": "assistant",
            "content": response
        }
    )