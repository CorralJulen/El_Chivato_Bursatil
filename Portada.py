import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA (Layout ancho y título) ---
st.set_page_config(
    page_title="El Chivato Bursátil | AI Fintech Platform",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 🎨 ESTILOS CSS "WOW FACTOR"
# ==============================================================================
st.markdown("""
<style>
    /* 1. FONDO GENERAL: Degradado sutil tecnológico */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* 2. FUENTES Y TIPOGRAFÍA */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1 {
        font-weight: 800 !important;
        color: #1a252f;
        font-size: 3rem !important;
        letter-spacing: -1px;
    }
    .big-subtitle {
        font-size: 1.3rem;
        color: #546e7a;
        margin-bottom: 30px;
    }

    /* 3. TARJETAS DE CARACTERÍSTICAS (Card UI) */
    .feature-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        height: 100%;
        position: relative;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }
    
    /* ESTILO ESPECIAL PARA LA TARJETA IA (La Joya de la Corona) */
    .feature-card-pro {
        border: 2px solid #8e44ad; /* Borde morado Gemini */
        background: linear-gradient(to bottom right, #ffffff, #fbf








