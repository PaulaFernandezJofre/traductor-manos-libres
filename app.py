import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

st.set_page_config(page_title="Traductor Manos Libres", page_icon="🗣️", layout="centered")
st.title("🎤 Traductor de Voz")

# -------------------------------
# Subir archivo de audio
# -------------------------------
audio_file = st.file_uploader("Sube un archivo de audio (wav o mp3)", type=["wav", "mp3"])

if audio_file is not None:
    st.audio(audio_file, format='audio/wav')
    
    # Guardar temporalmente el archivo
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_path = tmp_file.name

    # Reconocer voz
    r = sr.Recognizer()
    with sr.AudioFile(tmp_path) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="es-ES")
            st.success(f"Texto reconocido: {text}")
        except sr.UnknownValueError:
            st.error("No se pudo reconocer el audio")
        except sr.RequestError as e:
            st.error(f"Error al comunicarse con el servicio de Google: {e}")

    # -------------------------------
    # Convertir texto a voz
    # -------------------------------
    if 'text' in locals():
        tts = gTTS(text=text, lang='es')
        tts_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tts_file.name)
        st.audio(tts_file.name, format="audio/mp3")
        st.success("¡Traducción a voz generada con éxito!")