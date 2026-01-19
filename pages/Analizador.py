import streamlit as st
import pandas as pd
import datos
import calculos
import analisis_fundamental
import graficos

st.set_page_config(page_title="Semáforo Pro", page_icon="🚦", layout="wide")
st.title("🚦 Semáforo & Analizador Pro")

# --- 1. GESTIÓN DE MEMORIA (EL CEREBRO DE LA PÁGINA) ---
# Creamos la variable 'busqueda_activa' si no existe
if 'busqueda_activa' not in st.session_state:
    st.session_state['busqueda_activa'] = None

# Función para limpiar cuando pulsamos ranking
def activar_ranking():
    st.session_state['busqueda_activa'] = None

# --- 2. BOTONERA SUPERIOR ---
st.markdown("---")
col_izq, col_der = st.columns([2, 3])

with col_izq:
    st.subheader("Escáner General")
    st.write("Analiza las 60 empresas vigiladas.")
    # El botón ranking borra la búsqueda individual
    boton_ranking = st.button("🔄 Generar Ranking Completo", type="primary", use_container_width=True, on_click=activar_ranking)

with col_der:
    st.subheader("Buscador Específico")
    st.write("Busca por nombre o ticker (Ej: Amadeus, Amazon...)")
    
    c1, c2 = st.columns([3, 1])
    # Input simple
    texto_input = c1.text_input("Empresa", placeholder="Ej: Inditex", label_visibility="collapsed")
    # Botón simple
    if c2.button("🔍 Buscar"):
        # AQUÍ ESTÁ LA CLAVE: Si pulsas, guardamos el texto en la memoria a fuego
        if texto_input:
            st.session_state['busqueda_activa'] = texto_input
        else:
            st.warning("Escribe algo primero.")

st.markdown("---")

# ==============================================================================
# ESCENARIO A: HAY UNA BÚSQUEDA GUARDADA EN MEMORIA
# ==============================================================================
if st.session_state['busqueda_activa']:
    
    # Recuperamos el nombre de la memoria
    texto_a_buscar = st.session_state['busqueda_activa']
    
    # 1. Buscamos el Ticker oficial (Ej: Inditex -> ITX.MC)
    ticker_encontrado = datos.encontrar_ticker(texto_a_buscar)
    nombre_bonito = datos.NOMBRES.get(ticker_encontrado, ticker_encontrado)
    
    st.header(f"🔎 Informe: {nombre_bonito}")
    
    # 2. Descargamos Datos
    with st.spinner("Analizando mercado..."):
        df_hist = datos.descargar_datos([ticker_encontrado])
        
    # 3. Comprobamos si hay datos
    if df_hist.empty:
        st.error(f"❌ No he encontrado datos para '{ticker_encontrado}'. Prueba con el Ticker exacto (ej: AAPL, BBVA.MC).")
    else:
        try:
            # 4. Realizamos los cálculos
            nota_num, desglose = analisis_fundamental.analizar_calidad_fundamental(ticker_encontrado)
            estado_tec, mensaje_tec, precio, vol = calculos.analizar_semaforo(df_hist, ticker_encontrado)
            
            # Conversión Divisa
            moneda = "EUR"
            if not ticker_encontrado.endswith(".MC"):
                factor = datos.obtener_precio_dolar()
                precio = precio * factor
                moneda = "USD (Conv)"

            # Lógica de Color (Semáforo visual)
            color_nota = "red"
            if estado_tec == "VERDE":
                if nota_num >= 8: color_nota = "green"
                elif nota_num >= 5: color_nota = "orange"
            elif estado_tec == "NARANJA":
                color_nota = "orange"

            # --- VISUALIZACIÓN DEL INFORME ---
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Empresa", nombre_bonito)
            kpi2.metric("Precio Actual", f"{precio:.2f} €", delta=moneda)
            kpi3.markdown(f"""
                <div style='text-align: center; border: 2px solid {color_nota}; border-radius: 10px; background-color: rgba(255,255,255,0.1);'>
                    <h2 style='color: {color_nota}; margin:0;'>NOTA: {nota_num}/10</h2>
                </div>
            """, unsafe_allow_html=True)

            st.divider()

            g_col, t_col = st.columns([2, 1])
            
            with g_col:
                st.subheader("📈 Gráfico de Precios")
                try:
                    fig = graficos.crear_grafico_lineas(df_hist)
                    st.pyplot(fig)
                except: st.warning("Gráfico no disponible")

            with t_col:
                st.subheader("📝 Análisis")
                st.write(f"**Tendencia:** {estado_tec}")
                st.write(f"**Volatilidad:** {vol*100:.2f}%")
                
                if color_nota == "green": st.success("✅ OPORTUNIDAD DE COMPRA")
                elif color_nota == "orange": st.warning("⚠️ PRECAUCIÓN / MANTENER")
                else: st.error("⛔ NO INVERTIR AHORA")
                
                st.caption("Fundamental:")
                st.dataframe(pd.DataFrame(list(desglose.items()), columns=["Ratio", "Estado"]), hide_index=True)
                
        except Exception as e:
            st.error(f"Error al procesar los datos: {e}")

# ==============================================================================
# ESCENARIO B: NO HAY BÚSQUEDA -> MOSTRAMOS EL RANKING (Si se pulsa)
# ==============================================================================
elif boton_ranking: # Si pulsamos el botón de Ranking
    st.info("📡 Escaneando todas las empresas (Esto tarda unos segundos)...")
    
    try:
        df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
        factor = datos.obtener_precio_dolar()
        
        lista_final = []
        
        # Barra de progreso
        barra = st.progress(0)
        total = len(datos.EMPRESAS_SELECCIONADAS)
        
        for i, ticker in enumerate(datos.EMPRESAS_SELECCIONADAS):
            barra.progress((i+1)/total)
            try:
                # Análisis rápido
                estado, msg, precio, vol = calculos.analizar_semaforo(df_todos, ticker)
                nota, desglose = analisis_fundamental.analizar_calidad_fundamental(ticker)
                
                precio_fin = precio * factor if not ticker.endswith(".MC") else precio
                
                fila = {
                    "Empresa": datos.NOMBRES.get(ticker, ticker),
                    "Precio (€)": f"{precio_fin:.2f}",
                    "Tendencia": estado,
                    "Nota": nota,
                    "Puntos": nota # Para ordenar
                }
                # Añadimos los ratios fundamentales a la tabla
                fila.update(desglose)
                
                if estado != "ERROR":
                    lista_final.append(fila)
            except: pass
            
        barra.empty()
        
        # Filtros
        verdes = [x for x in lista_final if x["Tendencia"] == "VERDE" and x["Puntos"] >= 5]
        naranjas = [x for x in lista_final if x not in verdes and x["Tendencia"] != "ROJO"]
        rojas = [x for x in lista_final if x["Tendencia"] == "ROJO"]
        
        verdes.sort(key=lambda x: x["Puntos"], reverse=True)
        
        # --- TABLAS DE RESULTADOS ---
        # Definimos las columnas que queremos ver
        cols_ver = ["Empresa", "Precio (€)", "Tendencia", "Nota", "Valoración (PER)", "Rentabilidad", "Deuda"]
        
        st.success(f"🟢 TOP OPORTUNIDADES ({len(verdes)})")
        if verdes:
            t1, t2 = st.tabs(["Top 5", "Top 10"])
            with t1: st.dataframe(pd.DataFrame(verdes[:5])[cols_ver], use_container_width=True, hide_index=True)
            with t2: st.dataframe(pd.DataFrame(verdes[:10])[cols_ver], use_container_width=True, hide_index=True)
            
        st.warning(f"🟠 MIXTAS / PRECAUCIÓN ({len(naranjas)})")
        if naranjas:
            st.dataframe(pd.DataFrame(naranjas[:10])[cols_ver], use_container_width=True, hide_index=True)
            
        st.error(f"❌ TENDENCIA BAJISTA ({len(rojas)})")
        if rojas:
            st.dataframe(pd.DataFrame(rojas)[["Empresa", "Tendencia"]], use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error en el ranking: {e}")



