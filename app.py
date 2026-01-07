# app.py
import streamlit as st
from gtts import gTTS
import pyttsx3
import speech_recognition as sr
import os

st.set_page_config(page_title="Traductor con Voz", page_icon="🌐", layout="centered")
st.title("🌐 Traductor con voz - Streamlit")

st.markdown("""
Este traductor permite:
- Reconocer texto desde archivos de audio.
- Traducir texto escrito y escucharlo en voz.
""")

# -------------------------------------
# 1️⃣ Reconocimiento de voz desde archivo
# -------------------------------------
st.header("Reconocer voz desde archivo")
audio_file = st.file_uploader("Sube un archivo de audio (.wav o .mp3)", type=["wav", "mp3"])

if audio_file is not None:
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language="es-ES")
        st.success("Texto detectado:")
        st.write(text)
    except Exception as e:
        st.error(f"No se pudo reconocer el audio: {e}")

# -------------------------------------
# 2️⃣ Texto a voz
# -------------------------------------
st.header("Texto a voz")
text_input = st.text_area("Escribe el texto que quieres escuchar", "")

lang_option = st.selectbox("Selecciona el idioma para la voz (gTTS)", ["es", "en", "fr", "de", "it"], index=0)

if st.button("Reproducir texto"):
    if text_input.strip() == "":
        st.warning("Escribe algo primero")
    else:
        # Usamos gTTS para generar audio
        tts = gTTS(text=text_input, lang=lang_option)
        tts.save("temp.mp3")
        st.audio("temp.mp3", format="audio/mp3")
        # Limpiar archivo temporal
        os.remove("temp.mp3")

# -------------------------------------
# 3️⃣ Voz local (opcional) con pyttsx3
# -------------------------------------
st.header("Reproducir voz con pyttsx3 (local)")
if st.button("Probar pyttsx3"):
    engine = pyttsx3.init()
    engine.say("Hola, esta es una prueba de voz local")
    engine.runAndWait()
    st.info("Se ha reproducido un audio con pyttsx3 (funciona localmente, no en Streamlit Cloud)")

