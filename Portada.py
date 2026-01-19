import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA (Layout ancho y título) ---
st.set_page_config(
    page_title="El Chivato Bursátil | AI Fintech Platform",
    page_icon="📈",
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
        font-size: 3.5rem !important; /* Título gigante */
        letter-spacing: -1px;
    }
    h2 {
        font-weight: 600 !important;
        color: #2c3e50;
    }
    .big-subtitle {
        font-size: 1.5rem;
        color: #546e7a;
        margin-bottom: 30px;
    }

    /* 3. TARJETAS DE CARACTERÍSTICAS (Card UI) */
    .feature-card {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-10px); /* Efecto de elevación al pasar el ratón */
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
        border-color: #3498db;
    }
    .card-icon {
        font-size: 60px;
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 15px;
    }
    .card-text {
        color: #7f8c8d;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .fake-button {
        display: inline-block;
        margin-top: 25px;
        padding: 10px 25px;
        background-color: #f0f2f5;
        color: #2c3e50;
        border-radius: 30px;
        font-weight: 600;
        text-decoration: none;
    }

    /* 4. SECCIÓN DE HÉROE (BANNER) */
    .hero-container {
        padding: 20px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🚀 SECCIÓN HERO (EL PRIMER IMPACTO)
# ==============================================================================

# Imagen de Banner Ancha y Profesional (Bolsa/Tecnología)
# Usamos una imagen de Unsplash recortada panorámicamente
st.image(
    "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=2000&h=400&q=80",
    use_container_width=True,
)

# Título Principal y Subtítulo
st.markdown("""
    <div class="hero-container">
        <h1>El Chivato Bursátil AI</h1>
        <p class="big-subtitle">Tu ventaja competitiva en los mercados financieros. Inteligencia Artificial aplicada a la inversión.</p>
    </div>
""", unsafe_allow_html=True)

st.write("") # Espacio separador
st.write("")

# ==============================================================================
# 💎 LAS DOS HERRAMIENTAS PRINCIPALES (TARJETAS VISUALES)
# ==============================================================================
# Usamos columnas para presentar las dos funcionalidades clave de la app

col1, col2 = st.columns(2, gap="large")

with col1:
    # Tarjeta del Analizador
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Terminal de Análisis</div>
        <p class="card-text">
            Auditoría completa de activos en segundos. Combina análisis 
            <strong>Técnico</strong> (tendencias, volatilidad) y 
            <strong>Fundamental</strong> (salud financiera, dividendos) 
            potenciado por algoritmos de IA.
        </p>
        <div style="margin-top: 20px; color: #3498db; font-weight: bold;">
            👉 Accede desde el menú lateral: "Analizador"
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Tarjeta del Inversor
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">🤖</div>
        <div class="card-title">Robo-Advisor Inteligente</div>
        <p class="card-text">
            Gestión patrimonial automatizada. Define tu capital y tu 
            <strong>perfil de riesgo</strong>, y nuestro motor generará 
            una cartera diversificada y optimizada basada en reglas de calidad institucional.
        </p>
        <div style="margin-top: 20px; color: #3498db; font-weight: bold;">
            👉 Accede desde el menú lateral: "Inversor"
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")
st.divider()

# ==============================================================================
# 🏆 SECCIÓN DE CREDIBILIDAD (Por qué usar esto)
# ==============================================================================
st.subheader("🚀 ¿Por qué elegir nuestra plataforma?")
st.write("")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
        ### ⚡ Datos en Tiempo Real
        Conexión directa con mercados globales (NYSE, NASDAQ, BME) para decisiones al instante.
    """)

with c2:
    st.markdown("""
        ### 🧠 Algoritmos Propietarios
        No son simples medias móviles. Usamos modelos de puntuación multicriterio para filtrar el ruido.
    """)

with c3:
    st.markdown("""
        ### 🛡️ Enfoque en Calidad
        Priorizamos la preservación del capital. Solo las empresas financieramente sólidas pasan el corte.
    """)

st.write("")
st.write("")
st.markdown("---")
st.caption("© 2023-2024 El Chivato Bursátil AI Platforms. v2.5.0-stable. Powered by Python & Streamlit.")

# --- AÑADIR AL FINAL DE CADA ARCHIVO .PY ---

# --- Sustiuye el bloque anterior por este ---
with st.sidebar:
    st.markdown("---")
    st.markdown("### 👨‍💻 Sobre el Proyecto")
    st.caption("Desarrollado con ❤️ usando Python y Streamlit.")
    
    st.markdown("") 
    st.markdown("¿Te ha sido útil?")
    
    # TRUCO HTML: Botón que fuerza abrir el navegador externo
    # Nota: He puesto tu enlace https://paypal.me/JulenCorralLop
    st.markdown(
        """
        <a href="https://paypal.me/JulenCorralLop" target="_blank" style="text-decoration: none;">
            <div style="
                width: 100%;
                background-color: #FF4B4B;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                border: 1px solid #FF4B4B;">
                ☕ Invítame a un café
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )
    
    st.caption("v2.5.0 - Stable Release")
    
    st.caption("v2.5.0 - Stable Release")


