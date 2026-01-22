import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
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
    /* 1. FONDO GENERAL */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* 2. TIPOGRAFÍA */
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
        font-size: 1.2rem;
        color: #546e7a;
        margin-bottom: 30px;
    }

    /* 3. TARJETAS (Card UI) */
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
    
    /* Badge de "NUEVO" */
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
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🚀 SECCIÓN HERO
# ==============================================================================

st.image(
    "https://images.unsplash.com/photo-1642543492481-44e81e3914a7?auto=format&fit=crop&w=2000&q=80",
    use_container_width=True,
)

st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1>El Chivato Bursátil AI <span style='color:#8e44ad; font-size:2rem; vertical-align: top;'>✨</span></h1>
        <p class="big-subtitle">Tu ventaja competitiva en los mercados. Ahora con <strong>Inteligencia Artificial Generativa (Gemini 2.0)</strong>.</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 💎 LAS 3 HERRAMIENTAS (Ahora son 3 columnas)
# ==============================================================================

col1, col2, col3 = st.columns(3, gap="medium")

# --- COLUMNA 1: LA NUEVA ESTRELLA (IA) ---
with col1:
    st.markdown("""
    <div class="feature-card feature-card-pro">
        <div class="new-badge">NUEVO MOTOR v2</div>
        <div class="card-icon">🔮</div>
        <div class="card-title">Buscador IA + Radar</div>
        <p class="card-text">
            <strong>Lo más potente.</strong> Escribe "Zara" o "Google" y la IA encontrará el ticker, analizará noticias y te dará un veredicto.
            <br><br>
            Incluye <strong>Escáner Masivo</strong> para analizar 50 empresas a la vez.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.info("👉 Ve al menú lateral: **Buscador IA**")

# --- COLUMNA 2: EL CLÁSICO (ANALIZADOR) ---
with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Analizador Técnico</div>
        <p class="card-text">
            Auditoría matemática pura. Semáforos de valoración basados en PER, deuda y tendencias.
            <br><br>
            Ideal para ver los números fríos sin opiniones subjetivas.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("👉 Menú: **Analizador Técnico**")

# --- COLUMNA 3: EL GESTOR (ROBO-ADVISOR) ---
with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">🤖</div>
        <div class="card-title">Robo-Advisor</div>
        <p class="card-text">
            Gestión de carteras. Define tu capital y riesgo, y creamos una cesta de fondos/acciones diversificada.
            <br><br>
            Optimización de pesos basada en volatilidad.
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
    st.markdown("### ⚡ **Tiempo Real**\nConexión directa con NASDAQ y BME.")
with c2:
    st.markdown("### 🧠 **IA Generativa**\nMotor Google Gemini Flash integrado.")
with c3:
    st.markdown("### 🛡️ **Risk Manager**\nFiltros de calidad institucional.")

# ==============================================================================
# ☕ BARRA LATERAL (DONACIONES)
# ==============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=100) # Un logo chulo opcional
    st.markdown("### 👨‍💻 Apoya el proyecto")
    st.write("Si esta herramienta te ayuda a ganar dinero, ¡invítame a un café!")
    
    # QR DE PAYPAL (Centrado y bonito)
    st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://paypal.me/JulenCorralLop", caption="Escanear para donar")
    
    st.markdown("[☕ Invitar a un café (PayPal)](https://paypal.me/JulenCorralLop)")
    st.caption("v3.0.0 - AI Edition")







