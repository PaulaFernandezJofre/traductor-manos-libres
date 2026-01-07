import streamlit as st
import requests
import json

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="AAC Universal + IA Local",
    page_icon="🗣️",
    layout="centered"
)

st.title("🗣️ AAC Universal con Traducción IA Local")
st.write("Funciona desde PC, Android y iOS vía navegador.")

# =========================
# IDIOMAS
# =========================
LANGUAGES = {
    "Español": "Spanish",
    "English": "English",
    "Français": "French",
    "Deutsch": "German",
    "Italiano": "Italian",
    "Português": "Portuguese",
    "中文": "Chinese",
    "日本語": "Japanese",
    "한국어": "Korean",
    "العربية": "Arabic"
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

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    if r.status_code != 200:
        raise Exception("Ollama no disponible")

    return r.json()["response"].strip()

# =========================
# BOTÓN
# =========================
if st.button("🔊 Traducir y hablar"):
    if not text.strip():
        st.warning("Escribe un mensaje primero")
    else:
        try:
            translated_text = ollama_translate(
                text,
                LANGUAGES[source_lang],
                LANGUAGES[target_lang]
            )

            st.success("Texto traducido:")
            st.text_area("Resultado:", translated_text, height=100)

            # =========================
            # VOZ UNIVERSAL (NAVEGADOR)
            # =========================
            st.components.v1.html(
                f"""
                <script>
                const text = {translated_text};
                const msg = new SpeechSynthesisUtterance(text);

                // Detectar idioma automáticamente
                msg.lang = navigator.language || "en-US";

                window.speechSynthesis.cancel();
                window.speechSynthesis.speak(msg);
                </script>
                """,
                height=0
            )

        except Exception as e:
            st.error("Error al traducir con IA local")
            st.info(str(e))

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption(
    "AAC Universal · Traducción IA local con Ollama · "
    "Voz nativa del dispositivo · Multiplataforma"
)
st.caption("Desarrollado por Paula Fernández Jofré 2026")