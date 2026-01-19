import streamlit as st
import pandas as pd
import plotly.express as px
import datos
import calculos
import analisis_fundamental

# Configuración de página
st.set_page_config(page_title="Robo-Advisor Pro", page_icon="🤖", layout="wide")

# ==============================================================================
# 🎨 ZONA DE ESTILO (CSS INYECTADO)
# ==============================================================================
# Esto cambia el aspecto visual de la aplicación para que parezca más "Premium".
st.markdown("""
<style>
    /* 1. FONDO GENERAL DE LA APP (Patrón sutil + Degradado) */
    .stApp {
        background-color: #f0f2f6; /* Color base gris azulado */
        background-image: url("https://www.transparenttextures.com/patterns/cubes.png"); /* Patrón sutil */
        background-blend-mode: overlay;
    }

    /* 2. ESTILO DEL CONTENEDOR PRINCIPAL (Donde están los inputs) */
    /* Buscamos el bloque que contiene los inputs para darle estilo de "tarjeta" */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stNumberInput"]) {
        background-color: rgba(255, 255, 255, 0.95); /* Fondo blanco casi opaco */
        padding: 25px;
        border-radius: 15px; /* Bordes redondeados */
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); /* Sombra suave */
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }

    /* 3. BOTÓN PRINCIPAL MÁS LLAMATIVO */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #2980b9, #6dd5fa); /* Degradado azul */
        color: white;
        font-weight: bold;
        border: none;
        height: 50px; /* Más alto */
        font-size: 18px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.02); /* Efecto zoom al pasar el ratón */
        box-shadow: 0 6px 15px rgba(41, 128, 185, 0.4);
    }
    
    /* 4. TÍTULOS MÁS MODERNOS */
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 🏠 CABECERA Y TÍTULO
# ==============================================================================
# Imagen de banner para dar contexto "tech/finance"
st.image(
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=2070&q=80",
    use_container_width=True,
    height=200, # Altura fija para que sea un banner
)

st.title("🤖 El Inversor Inteligente")
st.markdown("""
<div style='background-color: rgba(255,255,255,0.7); padding: 10px; border-radius: 10px;'>
    Algoritmo de <b>Asignación de Activos</b>. Define tu perfil y distribuiremos tu capital 
    siguiendo estrictas reglas de <b>Calidad Fundamental y Control de Riesgo</b>.
</div>
""", unsafe_allow_html=True)

st.write("") # Espacio

# ==============================================================================
# 🎛️ ZONA DE CONFIGURACIÓN (ESTILO TARJETA)
# ==============================================================================
# El CSS de arriba hará que esta zona parezca una tarjeta blanca flotante
st.subheader("💼 Configura tu Inversión")

col1, col2 = st.columns(2)

with col1:
    capital = st.number_input("💰 Capital a invertir (€)", min_value=500.0, value=10000.0, step=100.0)

with col2:
    perfil = st.selectbox(
        "🧠 Perfil de Riesgo",
        options=["🐢 Conservador", "⚖️ Moderado", "🚀 Arriesgado"]
    )

# --- AVISOS DINÁMICOS ---
if "Arriesgado" in perfil:
    st.warning("⚠️ **¡ATENCIÓN!** Perfil de Alto Riesgo. Priorizaremos volatilidad alta. Existe riesgo de pérdida.")
else:
    st.info("ℹ️ **Estrategia Segura:** Selección basada en Tendencia Alcista (Técnico) y Solidez (Fundamental).")

st.write("") 

# --- BOTÓN DE ACCIÓN ---
# El CSS de arriba lo hará azul degradado y más grande
boton_generar = st.button("✨ GENERAR CARTERA OPTIMIZADA", type="primary", use_container_width=True)

st.markdown("---")

# ==============================================================================
# 🚀 LÓGICA PRINCIPAL (SE MANTIENE IGUAL)
# ==============================================================================
if boton_generar:
    
    st.write(f"### 📡 Diseñando cartera para perfil: **{perfil}**")
    
    # 1. Definición de Porcentajes
    if "Conservador" in perfil:
        pct_seguras, pct_medias, pct_picantes = 0.80, 0.20, 0.00
    elif "Moderado" in perfil:
        pct_seguras, pct_medias, pct_picantes = 0.60, 0.40, 0.00
    else: # Arriesgado
        pct_seguras, pct_medias, pct_picantes = 0.20, 0.40, 0.40

    # 2. Descarga
    try:
        with st.spinner("Conectando con mercados globales y analizando datos..."):
            df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
            factor_eur = datos.obtener_precio_dolar()
    except:
        st.error("Error de conexión con el mercado."); st.stop()
        
    barra = st.progress(0)
    todos_los_candidatos = []; cubo_seguras = []; cubo_medias = []; cubo_picantes = []  
    UMBRAL_BAJO = 0.010; UMBRAL_ALTO = 0.015

    for i, ticker in enumerate(datos.EMPRESAS_SELECCIONADAS):
        barra.progress((i+1)/len(datos.EMPRESAS_SELECCIONADAS))
        try:
            estado, _, precio, vol = calculos.analizar_semaforo(df_todos, ticker)
            if estado != "VERDE": continue
            nota, _ = analisis_fundamental.analizar_calidad_fundamental(ticker)
            precio_eur = precio * factor_eur if not ticker.endswith(".MC") else precio
            
            item = {"Empresa": datos.NOMBRES.get(ticker, ticker), "Precio": precio_eur, "Nota": nota, "Volatilidad": vol}
            todos_los_candidatos.append(item)
            
            if nota >= 7 and vol <= UMBRAL_BAJO: cubo_seguras.append(item)
            elif nota >= 7 and UMBRAL_BAJO < vol <= UMBRAL_ALTO: cubo_medias.append(item)
            elif vol > UMBRAL_ALTO: cubo_picantes.append(item)
        except: pass
    barra.empty()
    
    # --- 3. REPARTO ---
    cartera_final = []
    LABEL_SEGURIDAD = "🛡️ Seguridad (Nota>7)"
    LABEL_EQUILIBRIO = "⚖️ Equilibrio (Nota>7)"
    LABEL_RIESGO = "🔥 Riesgo (Volatilidad Alta)"
    
    def repartir_en_cubo(lista_candidatos, porcentaje_capital, nombre_bloque):
        if porcentaje_capital == 0: return
        dinero_disponible = capital * porcentaje_capital
        
        # Fallback
        if not lista_candidatos:
            if "Riesgo" in nombre_bloque:
                st.warning(f"⚠️ Mercado parado. Usando las más volátiles disponibles para Riesgo.")
                lista_candidatos = sorted(todos_los_candidatos, key=lambda x: x["Volatilidad"], reverse=True)[:3]
            elif "Equilibrio" in nombre_bloque and cubo_seguras: lista_candidatos = cubo_seguras
            else: return

        # Ordenar
        if "Riesgo" in nombre_bloque: lista_candidatos.sort(key=lambda x: x["Volatilidad"], reverse=True)
        else: lista_candidatos.sort(key=lambda x: x["Nota"], reverse=True)
            
        seleccion = lista_candidatos[:3]
        if not seleccion: return

        dinero_por_accion = dinero_disponible / len(seleccion)
        for accion in seleccion:
            num = int(dinero_por_accion / accion["Precio"])
            if num < 1: num = 1
            total = num * accion["Precio"]
            cartera_final.append({
                "Bloque": nombre_bloque, "Empresa": accion["Empresa"],
                "Nota": f"{accion['Nota']}/10", "Volatilidad": f"{accion['Volatilidad']*100:.2f}%",
                "Cantidad": num, "Total (€)": f"{total:.2f} €", "Total Inv.": total
            })

    repartir_en_cubo(cubo_seguras, pct_seguras, LABEL_SEGURIDAD)
    repartir_en_cubo(cubo_medias, pct_medias, LABEL_EQUILIBRIO)
    repartir_en_cubo(cubo_picantes, pct_picantes, LABEL_RIESGO)
    
    # --- 4. VISUALIZACIÓN ---
    if cartera_final:
        df_cartera = pd.DataFrame(cartera_final)
        total_invertido = df_cartera["Total Inv."].sum()
        
        st.success(f"✅ Cartera Generada. Inversión Total: {total_invertido:.2f} €")
        
        # Usamos un contenedor con fondo blanco para los resultados
        with st.container():
            st.markdown("<div style='background-color: rgba(255,255,255,0.9); padding: 20px; border-radius: 15px;'>", unsafe_allow_html=True)
            c1, c2 = st.columns([1, 2])
            with c1:
                st.subheader("Distribución Visual")
                mapa_colores = {LABEL_SEGURIDAD: "#2ecc71", LABEL_EQUILIBRIO: "#f39c12", LABEL_RIESGO: "#e74c3c", "(?)": "#95a5a6"}
                try:
                    fig = px.sunburst(df_cartera, path=['Bloque', 'Empresa'], values='Total Inv.', color='Bloque', color_discrete_map=mapa_colores)
                    st.plotly_chart(fig, use_container_width=True)
                except: st.warning("Gráfico interactivo no disponible.")
            with c2:
                st.subheader("📋 Lista de la Compra")
                st.dataframe(df_cartera[["Bloque", "Empresa", "Nota", "Volatilidad", "Cantidad", "Total (€)"]], use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("No se han encontrado acciones adecuadas hoy.")

