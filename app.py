import os
import streamlit as st
from groq import Groq
from PIL import Image

st.set_page_config(page_title="AI Fashion Stylist", layout="centered")
st.title("👗 AI Fashion Stylist")
st.markdown("Get fashion advice based on your outfit, event, and trends! Upload a photo if you like.")

# 🔑 Groq API Key from Hugging Face secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# 📤 Upload dress photo (optional)
uploaded_file = st.file_uploader("📸 (Optional) Upload a photo of your dress", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Uploaded Dress", use_container_width=True)

# 🎯 Fashion Inputs
st.subheader("🎯 Describe Your Look")
dress_type = st.selectbox("Dress Type", ["Frock", "Gown", "Saree", "Kurti", "Abaya", "Shirt & Trousers", "Other"])
event_type = st.selectbox("Occasion", ["Wedding", "Formal Dinner", "Eid", "Casual", "Party", "Work/Office"])
hair_length = st.selectbox("Hair Length", ["Short", "Medium", "Long"])
hair_texture = st.selectbox("Hair Texture", ["Straight", "Wavy", "Curly", "Coily"])
season = st.selectbox("Season", ["Summer", "Winter", "Spring", "Fall"])

# 🧠 Generate fashion advice with Groq LLaMA3
if st.button("✨ Get My Fashion Advice"):
    with st.spinner("Styling your look..."):
        prompt = (
            f"Suggest complete fashion styling for a {dress_type} suitable for a {event_type} in {season}. "
            f"The user has {hair_length.lower()} {hair_texture.lower()} hair. Recommend complementary jewelry, "
            f"makeup, purse, scarf, shoes, hairstyle, and color palette according to 2025 fashion trends."
        )
        if uploaded_file:
            prompt += " A photo of the dress was uploaded; assume it's modern and elegant."

        try:
            # 🔥 Model call to LLaMA3 (via Groq)
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant"
            )
            st.success("Your Personalized Fashion Advice:")
            st.markdown(response.choices[0].message.content)
            st.caption("🧠 Powered by LLaMA 3 (Groq API)")
        except Exception as e:
            st.error(f"❌ Error: {e}")
