import os
import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="Modal AI", layout="wide", page_icon="🤖")

# API Key Kontrolü & Kurulumu
gemini_api_key = st.secrets.get("AQ.Ab8RN6LGNzcfJXMbkwCVggMXPhGVkKzRDZPXBwwAvm9fWZzwhw") or os.getenv("AQ.Ab8RN6LGNzcfJXMbkwCVggMXPhGVkKzRDZPXBwwAvm9fWZzwhw")

if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
else:
    st.error("⚠️ API Anahtarı bulunamadı! Lütfen Streamlit Secrets veya .env dosyasına GEMINI_API_KEY ekleyin.")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

selected_mode = st.sidebar.radio("Mod Seçimi", ["💬 Metin Sohbeti", "🎨 Görsel Üretimi", "🎬 Video Üretimi"])

if selected_mode == "💬 Metin Sohbeti":
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Mesajınızı yazın...")
    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        if gemini_api_key:
            try:
                with st.spinner("AI yanıtı bekleniyor..."):
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(user_input)
                    assistant_message = response.text

                st.session_state["chat_history"].append({"role": "assistant", "content": assistant_message})
                with st.chat_message("assistant"):
                    st.markdown(assistant_message)
            except Exception as e:
                st.error(f"Yapay zeka yanıt üretirken bir hata oluştu: {e}")

elif selected_mode == "🎨 Görsel Üretimi":
    prompt = st.text_area("Görsel promptu girin.")
    if st.button("Üret"):
        st.info("İstek alındı, görsel modeli bir sonraki adımda bağlanacak")

elif selected_mode == "🎬 Video Üretimi":
    prompt = st.text_area("Video promptu girin.")
    if st.button("Üret"):
        st.info("İstek alındı, video modeli bir sonraki adımda bağlanacak")
      
