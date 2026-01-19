import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="El Chivato Bursátil",
    page_icon="📈",
    layout="wide"
)

# --- ENCABEZADO Y TÍTULO ---
st.title("🚀 El Chivato Bursátil")
st.markdown("### Tu copiloto inteligente para batir al mercado.")

# --- IMAGEN DE PORTADA (URL ESTABLE DE PIXABAY) ---
# Usamos una imagen directa .jpg para evitar errores de carga
try:
    st.image(
        "https://cdn.pixabay.com/photo/2016/11/27/21/42/stock-1863880_1280.jpg", 
        use_container_width=True,
        caption="Análisis Técnico y Fundamental al alcance de un clic."
    )
except:
    st.error("No se pudo cargar la imagen, pero el sistema funciona igual.")

st.markdown("---")

# --- INTRODUCCIÓN ---
st.markdown("""
Bienvenido a la herramienta definitiva para estudiantes e inversores. 
Este proyecto combina **Big Data**, **Análisis Financiero** y **Algoritmos de Riesgo** para simplificar la toma de decisiones.

¿Cómo funciona?
1.  **Analizamos:** Descargamos datos en tiempo real de España y EEUU.
2.  **Filtramos:** Aplicamos un "Semáforo" de tendencias y una auditoría fundamental.
3.  **Ejecutamos:** Diseñamos la cartera perfecta para tu perfil.
""")

st.markdown("---")

# --- NAVEGACIÓN A LAS PESTAÑAS (TARJETAS) ---
st.header("📍 ¿Por dónde quieres empezar?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚦 El Semáforo")
    st.write("Escáner de mercado que analiza tendencias (Técnico) y calidad (Fundamental). Descubre qué comprar y de qué huir.")
    
    # ENLACE 1: Apunta a Analizador.py
    st.page_link("pages/Analizador.py", label="Ir al Semáforo ->", icon="🚦", use_container_width=True)

with col2:
    st.markdown("### 🤖 Robo-Advisor")
    st.write("Algoritmo de gestión de carteras. Introduce tu capital y riesgo, y obtén una lista de compra optimizada.")
    
    # ENLACE 2: Apunta a Inversor.py
    st.page_link("pages/Inversor.py", label="Ir al Inversor ->", icon="🤖", use_container_width=True)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("🎓 Proyecto Final de Python | Diseñado con Streamlit y Yahoo Finance.")