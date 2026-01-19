import streamlit as st
import pandas as pd
import datos
import calculos
import analisis_fundamental
import graficos

st.set_page_config(page_title="Semáforo Pro", page_icon="🚦", layout="wide")
st.title("🚦 Semáforo & Analizador Pro")

# --- 🧠 GESTIÓN DE MEMORIA (CALLBACKS) ---
# Esta función se ejecuta JUSTO cuando das a Enter o click en Buscar
def guardar_busqueda():
    # Copiamos lo que has escrito en la caja a la memoria permanente
    if 'input_usuario' in st.session_state and st.session_state['input_usuario']:
        st.session_state['ticker_fijo'] = st.session_state['input_usuario']

def limpiar_busqueda():
    # Borramos la búsqueda individual para ver el ranking limpio
    st.session_state['ticker_fijo'] = None

# Inicializamos variables si no existen
if 'ticker_fijo' not in st.session_state:
    st.session_state['ticker_fijo'] = None

# --- ZONA SUPERIOR ---
st.markdown("---")
col_izq, col_der = st.columns([2, 3])

with col_izq:
    st.subheader("Escáner General")
    st.write("Analiza las 60 empresas vigiladas.")
    # El botón ranking limpia la búsqueda individual
    boton_ranking = st.button("🔄 Generar Ranking Completo", type="primary", use_container_width=True, on_click=limpiar_busqueda)

with col_der:
    st.subheader("Buscador Específico")
    st.write("Busca por nombre o ticker (Ej: Amadeus, Amazon...)")
    
    c_input, c_btn = st.columns([4, 1])
    
    # Caja de texto. Si das ENTER, se ejecuta guardar_busqueda
    texto = c_input.text_input(
        "Empresa", 
        placeholder="Ej: Inditex", 
        key="input_usuario", 
        on_change=guardar_busqueda, 
        label_visibility="collapsed"
    )
    
    # Botón. Si das CLICK, se ejecuta guardar_busqueda
    boton_buscar = c_btn.button("🔍 Buscar", on_click=guardar_busqueda)

st.markdown("---")

# ==============================================================================
# 🕵️‍♂️ LÓGICA DEL BUSCADOR INDIVIDUAL (Con memoria persistente)
# ==============================================================================
if st.session_state['ticker_fijo']:
    
    texto_a_buscar = st.session_state['ticker_fijo']
    
    # 1. Identificar Ticker
    ticker_encontrado = datos.encontrar_ticker(texto_a_buscar)
    nombre_bonito = datos.NOMBRES.get(ticker_encontrado, ticker_encontrado)
    
    st.header(f"🔎 Informe Financiero: {nombre_bonito}")
    
    with st.spinner(f"Analizando {nombre_bonito} a fondo..."):
        
        # A) Datos
        df_hist = datos.descargar_datos([ticker_encontrado])
        
        if df_hist.empty:
            st.error(f"❌ No he encontrado datos para '{ticker_encontrado}'. Prueba con otro nombre.")
        else:
            try:
                # B) Análisis
                nota_num, desglose = analisis_fundamental.analizar_calidad_fundamental(ticker_encontrado)
                estado_tec, mensaje_tec, precio, vol = calculos.analizar_semaforo(df_hist, ticker_encontrado)
                
                # C) Conversión Divisa
                if not ticker_encontrado.endswith(".MC"):
                    factor_eur = datos.obtener_precio_dolar()
                    precio_final = precio * factor_eur
                    moneda_origen = "USD"
                else:
                    precio_final = precio
                    moneda_origen = "EUR"

                # Lógica de colores
                if estado_tec == "ROJO": color_nota = "red"
                elif estado_tec == "NARANJA": color_nota = "orange"
                else:
                    if nota_num >= 8: color_nota = "green"
                    elif nota_num >= 5: color_nota = "orange"
                    else: color_nota = "red"

                # --- VISUALIZACIÓN ---
                c1, c2, c3 = st.columns(3)
                c1.metric("Empresa", nombre_bonito)
                c2.metric("Precio", f"{precio_final:.2f} €", delta=f"Origen: {moneda_origen}")
                
                c3.markdown(f"""
                    <div style='text-align: center; border: 2px solid {color_nota}; border-radius: 10px; padding: 5px; background-color: rgba(255,255,255,0.05);'>
                        <p style='margin:0; font-size: 14px;'>Nota Global</p>
                        <h1 style='color: {color_nota}; margin:0; font-size: 40px;'>{nota_num}/10</h1>
                    </div>
                """, unsafe_allow_html=True)

                st.divider()
                
                gc1, gc2 = st.columns([2, 1])
                with gc1:
                    st.subheader("📈 Gráfico 1 Año")
                    try:
                        fig = graficos.crear_grafico_lineas(df_hist)
                        st.pyplot(fig)
                    except: st.warning("Gráfico no disponible.")
                
                with gc2:
                    st.subheader("📝 Veredicto")
                    txt_tec = f"**Técnico:** Tendencia **{estado_tec}**. "
                    txt_tec += "Alta volatilidad." if vol > 0.025 else "Volatilidad normal."
                    
                    st.write(txt_tec)
                    
                    if color_nota == "green": st.success("✅ COMPRAR")
                    elif color_nota == "orange": st.warning("⚠️ PRECAUCIÓN")
                    else: st.error("⛔ NO TOCAR")
                    
                    st.caption("Detalles fundamentales:")
                    st.table(pd.DataFrame(list(desglose.items()), columns=["Ratio", "Valor"]))

            except Exception as e:
                st.error(f"Error analizando la empresa: {e}")

# ==============================================================================
# 🔄 LÓGICA DEL RANKING GENERAL (RESTUARADA LA ORIGINAL COMPLETA)
# ==============================================================================
elif boton_ranking:
    st.info("📡 Escaneando mercados de España y EEUU (Descarga Segura)...")
    
    try:
        df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
        factor_eur = datos.obtener_precio_dolar()
    except Exception as e:
        st.error(f"Error grave: {e}"); st.stop()
    
    candidatos = []; lista_roja = []
    barra = st.progress(0)
    
    # 1. Filtro Técnico (Semáforo)
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
    barra.empty()
    
    # 2. Filtro Fundamental (Auditoría Detallada)
    if candidatos:
        st.info(f"🔬 Auditando a {len(candidatos)} empresas candidatas...")
        verdes, naranjas = [], []
        barra2 = st.progress(0)
        
        for i, item in enumerate(candidatos):
            barra2.progress((i+1)/len(candidatos))
            try:
                # Recuperamos el análisis completo (Notas y Desglose)
                nota, desglose = analisis_fundamental.analizar_calidad_fundamental(item["Ticker"])
                
                item["Nota"] = f"{nota}/10"
                item["Puntuacion"] = nota
                item["Precio"] = f"{item['Precio']:.2f} €"
                # Añadimos todas las columnas del desglose al item
                item.update(desglose)
                
                if item["Estado"] == "VERDE":
                    if nota >= 5: verdes.append(item)
                    else: item["Motivo"] = "Fundamentales débiles"; naranjas.append(item)
                else: naranjas.append(item)
            except: pass
        barra2.empty()
        
        # Ordenamos por Puntuación
        verdes.sort(key=lambda x: x["Puntuacion"], reverse=True)
        naranjas.sort(key=lambda x: x["Puntuacion"], reverse=True)
        
        # Función auxiliar para mostrar tablas bonitas
        def mostrar(lista, n):
            if not lista: st.write("Sin datos.")
            else: 
                # Columnas detalladas que querías recuperar
                cols = ["Empresa", "Precio", "Nota", "Valoración (PER)", "Deuda", "Rentabilidad", "Crecimiento"]
                # Filtramos solo las columnas que existen en los datos
                df_mostrar = pd.DataFrame(lista[:n])
                # Aseguramos que solo mostramos columnas que existen (por si falla alguna descarga)
                cols_finales = [c for c in cols if c in df_mostrar.columns]
                st.dataframe(df_mostrar[cols_finales], use_container_width=True, hide_index=True)

        # --- MOSTRAR RESULTADOS ---
        st.success(f"🟢 OPORTUNIDADES ({len(verdes)})")
        if verdes:
            t1, t2 = st.tabs(["Top 5", "Top 10"])
            with t1: mostrar(verdes, 5)
            with t2: mostrar(verdes, 10)
            
        st.warning(f"🟠 RIESGO / MIXTO ({len(naranjas)})")
        if naranjas:
            t3, t4 = st.tabs(["Top 5", "Top 10"])
            with t3: mostrar(naranjas, 5)
            with t4: mostrar(naranjas, 10)
            
    st.error(f"❌ EVITAR ({len(lista_roja)})")
    if lista_roja: 
        st.dataframe(pd.DataFrame(lista_roja)[["Empresa", "Motivo"]], use_container_width=True, hide_index=True)

