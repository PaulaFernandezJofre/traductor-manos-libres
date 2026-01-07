import streamlit as st
from gtts import gTTS
import pyttsx3
import speech_recognition as sr

st.title("Traductor con voz")

# Subir archivo de audio
audio_file = st.file_uploader("Sube un archivo de audio", type=["wav", "mp3"])
if audio_file is not None:
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="es-ES")
            st.write("Texto detectado:", text)
        except Exception as e:
            st.write("No se pudo reconocer el audio:", e)

# Texto a voz
text_input = st.text_input("Escribe algo para escuchar")
if st.button("Reproducir"):
    tts = gTTS(text_input, lang="es")
    tts.save("temp.mp3")
    st.audio("temp.mp3", format="audio/mp3")
