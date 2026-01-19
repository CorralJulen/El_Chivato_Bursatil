import streamlit as st
import pandas as pd
import datos
import calculos
import analisis_fundamental
import graficos

st.set_page_config(page_title="Semáforo Pro", page_icon="🚦", layout="wide")
st.title("🚦 Semáforo & Analizador Pro")

# --- 1. GESTIÓN DE MEMORIA (EL CEREBRO DE LA PÁGINA) ---
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
        if texto_input:
            st.session_state['busqueda_activa'] = texto_input
        else:
            st.warning("Escribe algo primero.")

st.markdown("---")

# ==============================================================================
# ESCENARIO A: HAY UNA BÚSQUEDA GUARDADA (INDIVIDUAL)
# ==============================================================================
if st.session_state['busqueda_activa']:
    
    texto_a_buscar = st.session_state['busqueda_activa']
    
    ticker_encontrado = datos.encontrar_ticker(texto_a_buscar)
    nombre_bonito = datos.NOMBRES.get(ticker_encontrado, ticker_encontrado)
    
    st.header(f"🔎 Informe: {nombre_bonito}")
    
    with st.spinner("Analizando mercado..."):
        df_hist = datos.descargar_datos([ticker_encontrado])
        
    if df_hist.empty:
        st.error(f"❌ No he encontrado datos para '{ticker_encontrado}'. Prueba con el Ticker exacto.")
    else:
        try:
            nota_num, desglose = analisis_fundamental.analizar_calidad_fundamental(ticker_encontrado)
            estado_tec, mensaje_tec, precio, vol = calculos.analizar_semaforo(df_hist, ticker_encontrado)
            
            moneda = "EUR"
            if not ticker_encontrado.endswith(".MC"):
                factor = datos.obtener_precio_dolar()
                precio = precio * factor
                moneda = "USD (Conv)"

            color_nota = "red"
            if estado_tec == "VERDE":
                if nota_num >= 8: color_nota = "green"
                elif nota_num >= 5: color_nota = "orange"
            elif estado_tec == "NARANJA":
                color_nota = "orange"

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
# ESCENARIO B: RANKING GENERAL (RESTUARADO AL 100%)
# ==============================================================================
elif boton_ranking:
    # 1. Mensaje de carga inicial
    st.info("📡 Escaneando mercados de España y EEUU (Descarga Segura)...")
    
    try:
        # Descarga masiva
        df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
        factor_eur = datos.obtener_precio_dolar()
    except Exception as e:
        st.error(f"Error grave: {e}"); st.stop()
    
    candidatos = []; lista_roja = []
    
    # BARRA DE PROGRESO 1: ANÁLISIS TÉCNICO
    barra = st.progress(0)
    
    for i, ticker in enumerate(datos.EMPRESAS_SELECCIONADAS):
        barra.progress((i + 1) / len(datos.EMPRESAS_SELECCIONADAS))
        try:
            estado, mensaje, precio, vol = calculos.analizar_semaforo(df_todos, ticker)
            
            precio_final = precio * factor_eur if not ticker.endswith(".MC") else precio
            
            item = {
                "Ticker": ticker,
                "Empresa": datos.NOMBRES.get(ticker, ticker),
                "Precio": precio_final,
                "Estado": estado,
                "Motivo": mensaje
            }
            
            if estado == "ROJO": lista_roja.append(item)
            elif estado != "ERROR": candidatos.append(item) 
        except: pass
    barra.empty() # Quitamos la barra cuando acaba
    
    # 2. SEGUNDA FASE: AUDITORÍA FUNDAMENTAL
    if candidatos:
        st.info(f"🔬 Auditando a {len(candidatos)} empresas candidatas (Mirando balances)...")
        verdes, naranjas = [], []
        
        # BARRA DE PROGRESO 2: FUNDAMENTAL
        barra2 = st.progress(0)
        
        for i, item in enumerate(candidatos):
            barra2.progress((i+1)/len(candidatos))
            try:
                # Recuperamos el análisis completo
                nota, desglose = analisis_fundamental.analizar_calidad_fundamental(item["Ticker"])
                
                item["Nota"] = f"{nota}/10"
                item["Puntuacion"] = nota
                item["Precio"] = f"{item['Precio']:.2f} €"
                
                # AÑADIMOS EL DESGLOSE AL DICCIONARIO DEL ITEM
                # (Esto es lo que hace que salgan Dividendos, PER, etc.)
                item.update(desglose)
                
                if item["Estado"] == "VERDE":
                    if nota >= 5: verdes.append(item)
                    else: item["Motivo"] = "Fundamentales débiles"; naranjas.append(item)
                else: naranjas.append(item)
            except: pass
        barra2.empty()
        
        # Ordenamos
        verdes.sort(key=lambda x: x["Puntuacion"], reverse=True)
        naranjas.sort(key=lambda x: x["Puntuacion"], reverse=True)
        
        # Definimos las columnas que queremos ver (INCLUYENDO DIVIDENDOS)
        cols_ver = ["Empresa", "Precio", "Nota", "Valoración (PER)", "Rentabilidad", "Dividendos", "Deuda"]
        
        # Función para filtrar columnas que existan (por si alguna falla)
        def mostrar_tabla(lista, limite=None):
            if not lista: 
                st.write("Sin datos.")
                return
            
            df = pd.DataFrame(lista)




