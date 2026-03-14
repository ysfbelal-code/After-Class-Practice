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

if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

languages = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Korean": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Odia (Oriya)": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog (Filipino)": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}

language = st.selectbox("Enter the app language:", languages.keys())
st.session_state['language'] = language
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
