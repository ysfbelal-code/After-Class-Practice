import streamlit
from openai import OpenAI

def generate_response(prompt: str, temperature: float = 0.3, tokens: int = 1024):
    apikey = streamlit.secrets['groq_api']
    groq_url="https://api.groq.com/openai/v1"
    models = streamlit.secrets.get('GROQ_MODELS', ['llama-3.1-8b-instant', 'mixtral-8x7b-32768'])

    if not apikey:
        return "Error: groq_api missing in secrets"
    
    last_err = None
    for m in models:
        try:
            c = OpenAI(api_key=apikey, base_url=groq_url)
            r = c.chat.completions.create(
                model=m,
                messages = [{'role': 'user', 'content': prompt}], 
                temperature=temperature, 
                max_tokens=tokens
            )
            content =  r.choices[0].message.content
            if content is not None:
                return content
        
        except Exception as e:
            last_err = e
        
        if last_err is None:
            return "Error: no models available"
        
        return (
    "Hugging Face model failed."
    f"Tried models: {models}"
    "Fix:"
    "1) Switch to Hugging Face by inserting HF's models and changing to your HF API key, or"
    "2) Replace Groq model in MODELS.\n"
    f"Details: {type(last_err).__name__}: {last_err}"
)