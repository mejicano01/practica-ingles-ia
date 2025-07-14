import streamlit as st
import requests
from io import BytesIO
from gtts import gTTS

# --- Configuración Segura ---
st.set_page_config(
    page_title="Tutor de Inglés Seguro",
    page_icon="🛡️",
    layout="wide"
)

# --- Estilo Duolingo ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #58cc02;
    }
    .stButton>button {
        background: white !important;
        color: #58cc02 !important;
        border-radius: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Protección de Clave API ---
@st.cache_resource
def get_hf_key():
    # Accede al token desde Secrets de Streamlit
    try:
        return st.secrets["HUGGINGFACE_KEY"]
    except:
        st.error("🔐 Error: Configura el API Key en Secrets")
        st.stop()  # Detiene la app si no hay clave

HF_KEY = get_hf_key()  # Uso seguro del token

# --- Funciones Seguras ---
def procesar_audio(audio_bytes):
    """Envía audio a Whisper sin almacenarlo"""
    API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    
    # Validación de tamaño (máx 5MB)
    if len(audio_bytes.getvalue()) > 5_000_000:
        st.error("❌ Audio demasiado grande (máx 5MB)")
        return None
        
    response = requests.post(API_URL, headers=headers, data=audio_bytes.getvalue())
    return response.json().get("text") if response.status_code == 200 else None

# --- Interfaz ---
st.title("🗣️ Practica Inglés con IA Segura")
audio_file = st.file_uploader("Sube audio (.wav)", type=["wav"])

if audio_file:
    with st.spinner("🔍 Analizando..."):
        texto = procesar_audio(audio_file)
        
    if texto:
        st.success(f"🎤 Tú: {texto}")
        
        # Simulamos corrección sin otra API (para seguridad)
        correccion = texto.replace("goes", "went")  # Ejemplo básico
        st.warning(f"✏️ IA: ¿Quisiste decir: '{correccion}'?")
        
        # Generamos audio en memoria (sin guardar)
        audio_io = BytesIO()
        tts = gTTS(text=f"Did you mean: {correccion}?", lang="en")
        tts.write_to_fp(audio_io)
        st.audio(audio_io.getvalue())