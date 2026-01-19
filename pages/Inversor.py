import streamlit as st
import pandas as pd
import plotly.express as px
import datos
import calculos
import analisis_fundamental

st.set_page_config(page_title="Robo-Advisor Pro", page_icon="🤖", layout="wide")

st.title("🤖 El Inversor Inteligente")
st.markdown("""
Algoritmo de **Asignación de Activos**. 
Define tu perfil y distribuiremos tu capital siguiendo reglas estrictas de **Calidad y Riesgo**.
""")

st.markdown("---")

# ==============================================================================
# 🎛️ ZONA DE CONFIGURACIÓN (AHORA EN EL CENTRO)
# ==============================================================================
# Creamos un contenedor visual (opcional) o usamos columnas directamente
st.subheader("💼 Configura tu Inversión")

col1, col2 = st.columns(2)

with col1:
    capital = st.number_input("💰 Capital a invertir (€)", min_value=500.0, value=10000.0, step=100.0)

with col2:
    perfil = st.selectbox(
        "🧠 Perfil de Riesgo",
        options=["🐢 Conservador", "⚖️ Moderado", "🚀 Arriesgado"]
    )

# --- AVISOS DINÁMICOS (Justo debajo de los selectores) ---
if "Arriesgado" in perfil:
    st.warning("⚠️ **¡ATENCIÓN!** Perfil de Alto Riesgo. Priorizaremos la volatilidad. Puedes perder dinero.")
else:
    st.info("ℹ️ **Estrategia Segura:** Solo seleccionamos empresas con tendencia Alcista (Verde) y buena nota fundamental.")

st.write("") # Un poco de espacio

# --- BOTÓN DE ACCIÓN (Grande y ancho) ---
boton_generar = st.button("✨ GENERAR CARTERA OPTIMIZADA", type="primary", use_container_width=True)

st.markdown("---")

# ==============================================================================
# 🚀 LÓGICA PRINCIPAL (SE EJECUTA AL PULSAR EL BOTÓN)
# ==============================================================================
if boton_generar:
    
    st.write(f"### 📡 Diseñando cartera para perfil: **{perfil}**")
    
    # 1. Definición de Porcentajes
    if "Conservador" in perfil:
        pct_seguras = 0.80
        pct_medias = 0.20
        pct_picantes = 0.00
    elif "Moderado" in perfil:
        pct_seguras = 0.60
        pct_medias = 0.40
        pct_picantes = 0.00
    else: # Arriesgado
        pct_seguras = 0.20
        pct_medias = 0.40
        pct_picantes = 0.40

    # 2. Descarga y Análisis Masivo
    try:
        # Usamos st.spinner para que quede más elegante que la barra suelta
        with st.spinner("Analizando el mercado en tiempo real..."):
            df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
            factor_eur = datos.obtener_precio_dolar()
    except:
        st.error("Error conectando con mercado."); st.stop()
        
    # Barra de progreso visual
    barra = st.progress(0)
    
    # Listas
    todos_los_candidatos = [] 
    cubo_seguras = []   
    cubo_medias = []    
    cubo_picantes = []  

    # Umbrales
    UMBRAL_BAJO = 0.010 # 1.0%
    UMBRAL_ALTO = 0.015 # 1.5%

    for i, ticker in enumerate(datos.EMPRESAS_SELECCIONADAS):
        barra.progress((i+1)/len(datos.EMPRESAS_SELECCIONADAS))
        try:
            estado, _, precio, vol = calculos.analizar_semaforo(df_todos, ticker)
            
            # FILTRO: Solo queremos VERDES (Tendencia Alcista)
            if estado != "VERDE": continue
            
            nota, _ = analisis_fundamental.analizar_calidad_fundamental(ticker)
            precio_eur = precio * factor_eur if not ticker.endswith(".MC") else precio
            
            item = {
                "Empresa": datos.NOMBRES.get(ticker, ticker),
                "Precio": precio_eur,
                "Nota": nota,
                "Volatilidad": vol
            }
            
            todos_los_candidatos.append(item)
            
            # Clasificación en cubos
            if nota >= 7 and vol <= UMBRAL_BAJO:
                cubo_seguras.append(item)
            elif nota >= 7 and UMBRAL_BAJO < vol <= UMBRAL_ALTO:
                cubo_medias.append(item)
            elif vol > UMBRAL_ALTO:
                cubo_picantes.append(item)
                
        except: pass
        
    barra.empty()
    
    # --- 3. REPARTO DE DINERO ---
    cartera_final = []
    
    LABEL_SEGURIDAD = "🛡️ Seguridad (Nota>7)"
    LABEL_EQUILIBRIO = "⚖️ Equilibrio (Nota>7)"
    LABEL_RIESGO = "🔥 Riesgo (Volatilidad Alta)"
    
    def repartir_en_cubo(lista_candidatos, porcentaje_capital, nombre_bloque):
        if porcentaje_capital == 0: return
        
        dinero_disponible = capital * porcentaje_capital
        
        # Plan de emergencia (Fallback)
        if not lista_candidatos:
            if "Riesgo" in nombre_bloque:
                st.warning(f"⚠️ Mercado muy parado. Usando las más volátiles disponibles para el bloque de Riesgo.")
                lista_maestra_ordenada = sorted(todos_los_candidatos, key=lambda x: x["Volatilidad"], reverse=True)
                lista_candidatos = lista_maestra_ordenada[:3]
            elif "Equilibrio" in nombre_bloque and cubo_seguras:
                 lista_candidatos = cubo_seguras
            else:
                return

        # Ordenar
        if "Riesgo" in nombre_bloque:
            lista_candidatos.sort(key=lambda x: x["Volatilidad"], reverse=True)
        else:
            lista_candidatos.sort(key=lambda x: x["Nota"], reverse=True)
            
        seleccion = lista_candidatos[:3]
        if not seleccion: return

        dinero_por_accion = dinero_disponible / len(seleccion)
        
        for accion in seleccion:
            num = int(dinero_por_accion / accion["Precio"])
            if num < 1: num = 1
            total = num * accion["Precio"]
            
            cartera_final.append({
                "Bloque": nombre_bloque,
                "Empresa": accion["Empresa"],
                "Nota": f"{accion['Nota']}/10",
                "Volatilidad": f"{accion['Volatilidad']*100:.2f}%",
                "Cantidad": num,
                "Total (€)": f"{total:.2f} €",
                "Total Inv.": total
            })

    repartir_en_cubo(cubo_seguras, pct_seguras, LABEL_SEGURIDAD)
    repartir_en_cubo(cubo_medias, pct_medias, LABEL_EQUILIBRIO)
    repartir_en_cubo(cubo_picantes, pct_picantes, LABEL_RIESGO)
    
    # --- 4. VISUALIZACIÓN FINAL ---
    if cartera_final:
        df_cartera = pd.DataFrame(cartera_final)
        total_invertido = df_cartera["Total Inv."].sum()
        
        st.success(f"✅ Cartera Generada con éxito. Inversión Real: {total_invertido:.2f} €")
        
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.subheader("Distribución Visual")
            
            mapa_colores = {
                LABEL_SEGURIDAD: "#2ecc71",  # Verde
                LABEL_EQUILIBRIO: "#f39c12", # Naranja
                LABEL_RIESGO: "#e74c3c",     # Rojo
                "(?)": "#95a5a6"
            }
            
            try:
                fig = px.sunburst(
                    df_cartera, 
                    path=['Bloque', 'Empresa'], 
                    values='Total Inv.', 
                    color='Bloque', 
                    color_discrete_map=mapa_colores
                )
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.warning("Gráfico interactivo no disponible.")

        with c2:
            st.subheader("📋 Tu Lista de la Compra")
            st.dataframe(
                df_cartera[["Bloque", "Empresa", "Nota", "Volatilidad", "Cantidad", "Total (€)"]],
                use_container_width=True,
                hide_index=True
            )
    else:
        st.error("No se han encontrado acciones que cumplan los criterios hoy.")
