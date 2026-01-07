import streamlit as st
import requests
from gtts import gTTS
import base64
import tempfile
import os
import json

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="AAC Universal Web Híbrido",
    page_icon="🗣️",
    layout="centered"
)

st.title("🗣️ AAC Universal Web · Híbrido")
st.write("Funciona en PC, Android y iOS vía navegador, con voz adaptativa.")

# =========================
# IDIOMAS
# =========================
LANGUAGES = {
    "Español": "es",
    "English": "en",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    "Português": "pt",
    "中文": "zh",
    "日本語": "ja",
    "한국어": "ko",
    "العربية": "ar"
}

# =========================
# UI
# =========================
text = st.text_area("✍️ Mensaje:", height=150)
source_lang = st.selectbox("Idioma original", LANGUAGES.keys(), index=0)
target_lang = st.selectbox("Idioma de salida", LANGUAGES.keys(), index=1)

# =========================
# OLLAMA TRANSLATION
# =========================
def ollama_translate(text, source, target):
    prompt = (
        f"Translate the following text from {source} to {target}. "
        f"Only return the translated text.\n\n{text}"
    )
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1:8b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        st.warning(f"No se pudo usar Ollama: {e}")
        return text  # Devuelve el texto original si falla

# =========================
# FUNCIÓN gTTS
# =========================
def speak_text(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)

        with open(tmp_file.name, "rb") as f:
            audio_bytes = f.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        """
        st.components.v1.html(audio_html, height=50)
    except Exception as e:
        st.error(f"Error al generar audio con gTTS: {e}")
    finally:
        try:
            os.unlink(tmp_file.name)
        except:
            pass

# =========================
# SESIÓN PARA FALLBACK gTTS
# =========================
if "tts_fallback" not in st.session_state:
    st.session_state["tts_fallback"] = False

# =========================
# BOTÓN HÍBRIDO
# =========================
if st.button("🔊 Traducir"):
    if not text.strip():
        st.warning("Escribe un mensaje primero")
    else:
        translated_text = ollama_translate(
            text,
            LANGUAGES[source_lang],
            LANGUAGES[target_lang]
        )

        st.success("Texto traducido:")
        st.text_area("Resultado:", translated_text, height=100)

        # =========================
        # VOZ HÍBRIDA
        # =========================
        st.components.v1.html(
            f"""
            <script>
            function playVoice(text, lang) {{
                if ('speechSynthesis' in window) {{
                    const msg = new SpeechSynthesisUtterance(text);
                    msg.lang = lang;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(msg);
                }} else {{
                    fetch(window.location.href, {{
                        method: "POST",
                        headers: {{
                            "Content-Type": "application/json"
                        }},
                        body: JSON.stringify({{tts_fallback: true}})
                    }});
                }}
            }}
            playVoice({json.dumps(translated_text)}, '{LANGUAGES[target_lang]}');
            </script>
            """,
            height=0
        )

        # =========================
        # gTTS fallback
        # =========================
        if st.session_state.get("tts_fallback", False):
            speak_text(translated_text, LANGUAGES[target_lang])
            st.session_state["tts_fallback"] = False

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption(
    "AAC Universal Web · Traducción IA local con Ollama · "
    "Voz del navegador + gTTS · Híbrido y multiplataforma"
)
st.caption("Desarrollado por Paula Fernández Jofré 2026")
