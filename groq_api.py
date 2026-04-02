import streamlit as st
from openai import OpenAI

@st.cache_data(show_spinner=False)

def generate_response(prompt: str, temperature: float = 0.3, tokens: int = 8192) -> str:
    url = "https://api.groq.com/openai/v1"
    apikey = st.secrets['hf_api']
    models = st.secrets.get('GROQ_MODELS', 
                            ['meta-llama/llama-4-scout-17b-16e-instruct', 
                            'llama-3.1-8b-instant', 
                            'llama-3.3-70b-versatile',])
    
    if not apikey:
        return "Error: hf_api missing in secrets"

    last_err = None
    for m in models:
        try:
            c = OpenAI(api_key=apikey, base_url=url)
            r = c.chat.completions.create(
                model=m,
                messages=[{'role':'system', "content": "You follow instructions exactly. Output ONLY what is asked — no preamble, no explanation, no extra text. If there's a word with multiple meanings in the other language, output the first thing that comes to mind. Make sure the translations are gramatically correct. Avoid outputs like \frac{2420}{20} when solving equations. USe the actual mathematical symbols if you can, and make sure they don't overlap the page or don't fully appear."}, 
                {'role': 'user', 'content': prompt}],
                temperature=temperature,
                max_tokens=tokens
            )

            content = r.choices[0].message.content
            if content is not None:
                return content
            
        except Exception as e:
            last_err = e

    if last_err is None:
        return "Error: no models available"

    return (
        "Groq model failed."
        f"Tried models: {models}"
        "Fix:"
        "1) Switch to HF by inserting HF's models and changing to your HF API key, or"
        "2) Replace Groq model in MODELS.\n"
        f"Details: {type(last_err).__name__}: {last_err}"
    )
