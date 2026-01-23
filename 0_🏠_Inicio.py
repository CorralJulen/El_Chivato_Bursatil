import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="El Chivato Bursátil | AI Fintech Platform",
    page_icon="🐂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 🎨 ESTILOS CSS (Cuidado: Asegúrate de copiar todo este bloque)
# ==============================================================================
st.markdown("""
<style>
    /* 1. FONDO GENERAL */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* 2. FUENTES */
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

    /* 3. TARJETAS */
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
    
    /* TARJETA IA (Destacada) */
    .feature-card-pro {
        border: 2px solid #8e44ad;
        background: linear-gradient(to bottom right, #ffffff, #fbfcd4);
    }
    
    .card-icon {
        font-size: 50px;
        margin-bottom: 15px;
    }
    .card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .card-text {
        color: #7f8c8d;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Badge NUEVO */
    .new-badge {
        background-color: #e74c3c;
        color: white;
        padding: 4px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: bold;
        position: absolute;
        top: 10px;
        right: 10px;
    }

    /* BANNER */
    .hero-container {
        padding: 20px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True) 
# ⬆️ ¡ESTAS COMILLAS DE ARRIBA SON LAS IMPORTANTES!

# ==============================================================================
# 🚀 SECCIÓN HERO
# ==============================================================================

# Imagen Financiera Profesional
st.image(
    "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=2000&q=80",
    use_container_width=True,
)

st.markdown("""
    <div class="hero-container">
        <h1>El Chivato Bursátil AI <span style='color:#8e44ad; font-size:2rem; vertical-align: top;'>✨</span></h1>
        <p class="big-subtitle">Tu ventaja competitiva en los mercados. Inteligencia Artificial (Gemini 2.0) aplicada a la inversión.</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 💎 LAS 3 HERRAMIENTAS
# ==============================================================================

col1, col2, col3 = st.columns(3, gap="medium")

# --- 1. IA ---
with col1:
    st.markdown("""
    <div class="feature-card feature-card-pro">
        <div class="new-badge">NUEVO MOTOR v2</div>
        <div class="card-icon">🔮</div>
        <div class="card-title">Buscador IA + Radar</div>
        <p class="card-text">
            <strong>Lo más potente.</strong> Escribe "Zara" o "Google" y la IA encontrará el ticker y analizará noticias.
            <br><br>
            Incluye <strong>Escáner Masivo</strong> de oportunidades.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.info("👉 Menú: **Buscador IA**")

# --- 2. ANALIZADOR ---
with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Analizador Técnico</div>
        <p class="card-text">
            Auditoría matemática pura. Semáforos de valoración basados en PER, deuda y tendencias.
            <br><br>
            Números fríos sin opiniones subjetivas.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("👉 Menú: **Analizador Técnico**")

# --- 3. ROBO-ADVISOR ---
with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">🤖</div>
        <div class="card-title">Robo-Advisor</div>
        <p class="card-text">
            Gestión de carteras. Define tu capital y riesgo, y creamos una cesta diversificada.
            <br><br>
            Optimización de pesos por volatilidad.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("👉 Menú: **Robo-Advisor**")

st.divider()

# ==============================================================================
# 🏆 CREDIBILIDAD
# ==============================================================================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### ⚡ **Tiempo Real**\nConexión directa con mercados globales.")
with c2:
    st.markdown("### 🧠 **IA Google**\nMotor Gemini Flash integrado.")
with c3:
    st.markdown("### 🛡️ **Calidad**\nSolo empresas financieramente sólidas.")

st.markdown("---")

# ==============================================================================
# ☕ BARRA LATERAL
# ==============================================================================
with st.sidebar:
    st.markdown("### 👨‍💻 Apoya el proyecto")
    st.write("Si el Chivato te ayuda, ¡invítame a un café!")
    
    st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://paypal.me/JulenCorralLop", caption="Escanear para donar")
    st.markdown("[☕ Enlace PayPal](https://paypal.me/JulenCorralLop)")
    
    st.markdown("---")
    st.caption("© 2024 El Chivato Bursátil AI. v3.0.0")