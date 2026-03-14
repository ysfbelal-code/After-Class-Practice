import streamlit as st
from groq_api import generate_response
import io

st.session_state.setdefault("conversation", [])

st.markdown("""
<style>
@import url('');

html, body, [class*="css"], [class*="st-"], .stApp, .stApp * {
    font-family: 'Yu Gothic UI Light', Yu, sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

st.title("ENHANCED AI TEACHING ASSISTANT", text_alignment='center')


c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    clear = st.button("Clear conversation history")
with c2:
    view = st.button("View conversation history")
with c3:
    export = st.button("Export conversation history")

role = st.selectbox("Choose the style of the AI's response:", ("Teacher", "Professor", "Friendly Helper"))
user_question = st.text_input("How can I help you today?")

if clear:
    if st.session_state.conversation:
        st.session_state.conversation = []
        st.toast("Conversation history cleared!")
    else:
        st.toast("Conversation history is already empty.")
elif view:
    if st.session_state.conversation:
        st.markdown("Conversation History:")
        for i, chat in enumerate(st.session_state.conversation, 1):
            st.markdown(f"{i}:")
            st.markdown(f"You: {chat['question']}")
            st.markdown(f"AI {chat['role']}: {chat['answer']}")
            st.markdown('---')
    else:
        st.toast("Conversation history is empty.")
elif export:
    def export_bytes(history):
        text = "".join([f"Q{i}: {chat['question']}\nA{i}:{chat['answer']}\n\n" for i, chat in enumerate(st.session_state.conversation, 1)])
        return io.BytesIO(text.encode("utf-8"))
    if st.session_state.conversation:
        st.download_button(
            label="Export Chat History",
            data = export_bytes(st.session_state.conversation),
            file_name="Enhanced_AI_Teaching_Assistant_Conversation.txt", 
            mime="text/plain"
        )
    else:
        st.toast("Conversation history is empty.")

elif user_question:
    if user_question.strip():
        prompt = f"You are a {role}. Please answer the following question: {user_question}"
        with st.spinner("Generating answer..."):
            answer = st.markdown(generate_response(prompt, temperature=0.3, tokens=1024))
        st.session_state.conversation.append({'role':role, 'question':user_question.strip(), 'answer':answer})
    else:
        st.warning("⚠️ Please enter a question if you want to use this AI.")
