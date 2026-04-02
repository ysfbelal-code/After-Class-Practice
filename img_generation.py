from groq_api import generate_response
from io import BytesIO
import requests, streamlit as st
from huggingface_hub import InferenceClient
from config import hf_api_key

MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
FILTER_API_URL = "https://filters-zeta.vercel.app/api/filter"

ENHANCE_SYS = (
    "Improve prompts for text-to-image generation. Return ONLY the enhanced prompt."
    "Add subject, style, lighting, camera angle, colours, background. Keep it safe."
)

# For image quality guidance only
NEGATIVE = "low quality, blurry, distorted, watermark, text, cropped"

img_client = InferenceClient(provider="hf-inference", api_key=hf_api_key)

def check_prompt(prompt: str):
    try:
        response = requests.post(
            FILTER_API_URL, 
            json={'prompt':prompt}, 
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            return {'ok': False, 'reason': 'Invalid filter API response.'}
        
        return data
    
    except Exception as e:
        return {
            'ok': False, 
            'reason': f"Filter API error: {str(e)}"
        }
    
def enhance_prompt(raw: str) -> str:
    out = generate_response(
        f"{ENHANCE_SYS}\nUser prompt: {raw}",
        temperature=0.4, 
        tokens=220
    )
    return (out or raw).strip()

def gen_image(prompt: str):
    filter_result = check_prompt(prompt)
    if not filter_result.get('ok'):
        return None, f"Prompt blocked by safety filter. {filter_result.get('reason', 'Unsafe prompt')}"
    
    try:
        return img_client.text_to_image(
            prompt=prompt, 
            negative_prompt=NEGATIVE, 
            model=MODEL_ID
        ), None

    except Exception as e:
        msg = str(e)

        if "negative_prompt" in msg or "unexpected keyword" in msg:
            try:
                return img_client.text_to_image(
                    prompt=prompt,
                    model=MODEL_ID
                ), None
            except Exception as e2:
                msg = str(e2)
        
        if any(x in msg for x in ['402', 'Payment Required', 'pre-paid credits']):
            return None, "Image backend requires credits or model not available on hf-inference.\n"
        
        if "404" in msg or "Not Found" in msg:
            return None, "Model not served on this provider route (hf-inference).\n\nRaw error: " + msg
        
        return None, "Error during image generation: " + msg

def main():
    st.set_page_config(page_title="Safe AI Image Generator", layout="centered")
    st.title("Safe AI Image Generator")
    st.info("Flow: Enter a prompt -> enhance it -> check it using the deployed safety API -> generate the image.")

    with st.form('image_form'):
        raw = st.text_area(
            "Image Description", 
            height=120, 
            placeholder="Example: A haunted manor surrounded by dead trees and decaying grass, low lighting"
        )
        submit = st.form_submit_button("Generate Image")
    
    if submit:
        raw = raw.strip()

        if not raw:
            st.warning("Please enter an image description.")
            return
        
        raw_check = check_prompt(raw)
        if not raw_check.get('ok'):
            st.error(f"Prompt blocked. {raw_check.get('reason', 'Unsafe prompt')}")
            return
        
        with st.spinner("Enhancing your prompt..."):
            final_prompt = enhance_prompt(raw)

        enhanced_check = check_prompt(final_prompt)
        if not enhanced_check.get('ok'):
            st.error(f"Prompt blocked. {raw_check.get('reason', 'Unsafe prompt')}")
            return
        
        st.markdown("---Enhanced Prompt---")
        st.code(final_prompt)

        with st.spinner("Generating image..."):
            img, err = gen_image(final_prompt)

        if err:
            st.error(err)
            return
        
        st.image(img, caption="Generated Image", use_container_width=True)
        st.session_state.generated_image = img

    img = st.session_state.get("generated_image")
    if img:
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            "Download Image", 
            buf.getvalue(), 
            "ai_generated_image.png", 
            "image/png"
        )

if __name__ == "__main__":
    main()