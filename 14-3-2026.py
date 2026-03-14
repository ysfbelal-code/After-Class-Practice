import streamlit as st
from groq_api import generate_response
import time

st.markdown("""
    <style>
            html, body [class*='css'] {
            font-family: 'Times New Roman', monospace;
            font-size: 18px;
            }
    </style>""", unsafe_allow_html=True
)

st.session_state.setdefault("conversation", [])
st.title("ENHANCED AI TEACHING ASSISTANT", text_alignment='center')
st.text_input("How can I help you today?")

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    clear = st.button("Clear conversation history")
with c2:
    view = st.button("View conversation history")
with c3:
    export = st.button("Export conversation history")
