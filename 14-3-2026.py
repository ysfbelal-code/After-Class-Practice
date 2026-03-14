import streamlit as st
from groq_api import generate_response, translate_text
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

# ── Language setup ─────────────────────────────────────────────────────────────
languages = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar",
    "Armenian": "hy", "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be",
    "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg", "Catalan": "ca",
    "Cebuano": "ceb", "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Corsican": "co", "Croatian": "hr", "Czech": "cs", "Danish": "da",
    "Dutch": "nl", "English": "en", "Esperanto": "eo", "Estonian": "et",
    "Finnish": "fi", "French": "fr", "Frisian": "fy", "Galician": "gl",
    "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu",
    "Haitian Creole": "ht", "Hausa": "ha", "Hawaiian": "haw", "Hebrew": "he",
    "Hindi": "hi", "Hmong": "hmn", "Hungarian": "hu", "Icelandic": "is",
    "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it",
    "Japanese": "ja", "Javanese": "jv", "Kannada": "kn", "Kazakh": "kk",
    "Khmer": "km", "Kinyarwanda": "rw", "Korean": "ko", "Kurdish": "ku",
    "Kyrgyz": "ky", "Lao": "lo", "Latin": "la", "Latvian": "lv",
    "Lithuanian": "lt", "Luxembourgish": "lb", "Macedonian": "mk", "Malagasy": "mg",
    "Malay": "ms", "Malayalam": "ml", "Maltese": "mt", "Maori": "mi",
    "Marathi": "mr", "Mongolian": "mn", "Myanmar (Burmese)": "my", "Nepali": "ne",
    "Norwegian": "no", "Nyanja (Chichewa)": "ny", "Odia (Oriya)": "or", "Pashto": "ps",
    "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa",
    "Romanian": "ro", "Russian": "ru", "Samoan": "sm", "Scots Gaelic": "gd",
    "Serbian": "sr", "Sesotho": "st", "Shona": "sn", "Sindhi": "sd",
    "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl", "Somali": "so",
    "Spanish": "es", "Sundanese": "su", "Swahili": "sw", "Swedish": "sv",
    "Tagalog (Filipino)": "tl", "Tajik": "tg", "Tamil": "ta", "Tatar": "tt",
    "Telugu": "te", "Thai": "th", "Turkish": "tr", "Turkmen": "tk",
    "Ukrainian": "uk", "Urdu": "ur", "Uyghur": "ug", "Uzbek": "uz",
    "Vietnamese": "vi", "Welsh": "cy", "Xhosa": "xh", "Yiddish": "yi",
    "Yoruba": "yo", "Zulu": "zu",
}

if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

# Sidebar language selector — rendered ONCE
language = st.sidebar.selectbox(
    "App language:",
    list(languages.keys()),
    index=list(languages.keys()).index(st.session_state['language'])
)
st.session_state['language'] = language
lang = language  # shorthand used below

# ── Title & action buttons (rendered ONCE) ────────────────────────────────────
st.title(translate_text("ENHANCED AI TEACHING ASSISTANT", lang))

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    clear = st.button(translate_text("Clear conversation history", lang))
with c2:
    view = st.button(translate_text("View conversation history", lang))
with c3:
    export = st.button(translate_text("Export conversation history", lang))

# ── Main widgets — rendered ONCE each ────────────────────────────────────────
role = st.selectbox(
    translate_text("Choose the style of the AI's response:", lang),
    (
        translate_text("Teacher", lang),
        translate_text("Professor", lang),
        translate_text("Friendly Helper", lang),
    )
)

user_question = st.text_input(translate_text("How can I help you today?", lang))

# ── Button / input logic ──────────────────────────────────────────────────────
if clear:
    if st.session_state.conversation:
        st.session_state.conversation = []
        st.toast(translate_text("Conversation history cleared!", lang))
    else:
        st.toast(translate_text("Conversation history is already empty.", lang))

elif view:
    if st.session_state.conversation:
        st.markdown(translate_text("Conversation History:", lang))
        for i, chat in enumerate(st.session_state.conversation, 1):
            st.markdown(f"{i}:")
            st.markdown(f"{translate_text('You', lang)}: {chat['question']}")
            st.markdown(f"AI {chat['role']}: {chat['answer']}")
            st.markdown("---")
    else:
        st.toast(translate_text("Conversation history is empty.", lang))

elif export:
    def export_bytes(history):
        text = "".join([
            f"Q{i}: {chat['question']}\nA{i}: {chat['answer']}\n\n"
            for i, chat in enumerate(st.session_state.conversation, 1)
        ])
        return io.BytesIO(text.encode("utf-8"))

    if st.session_state.conversation:
        st.download_button(
            label=translate_text("Export Chat History", lang),
            data=export_bytes(st.session_state.conversation),
            file_name="Enhanced_AI_Teaching_Assistant_Conversation.txt",
            mime="text/plain"
        )
    else:
        st.toast(translate_text("Conversation history is empty.", lang))

elif user_question:
    if user_question.strip():
        # Send the prompt in English — translate the ANSWER for display
        prompt = f"You are a {role}. Please answer the following question: {user_question}"
        with st.spinner(translate_text("Generating answer...", lang)):
            answer = generate_response(prompt, temperature=0.3, tokens=1024)
        translated_answer = translate_text(answer, lang)
        st.markdown(translated_answer)
        st.session_state.conversation.append({
            'role': role,
            'question': user_question.strip(),
            'answer': translated_answer
        })
    else:
        st.warning(translate_text("⚠️ Please enter a question if you want to use this AI.", lang))

st.rerun()
