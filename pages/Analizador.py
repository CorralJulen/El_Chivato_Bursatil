import streamlit as st
import pandas as pd
import datos
import calculos
import analisis_fundamental
import graficos

st.set_page_config(page_title="Semáforo Pro", page_icon="🚦", layout="wide")
st.title("🚦 Semáforo & Analizador Pro")

# --- MEMORIA DE SESIÓN (ESTO EVITA EL PARPADEO) ---
# Inicializamos la variable 'empresa_seleccionada' si no existe
if 'empresa_seleccionada' not in st.session_state:
    st.session_state['empresa_seleccionada'] = None

# --- ZONA SUPERIOR ---
st.markdown("---")
col_izq, col_der = st.columns([2, 3])

with col_izq:
    st.subheader("Escáner General")
    st.write("Analiza las 60 empresas vigiladas.")
    # Callback para limpiar la búsqueda si usamos el ranking
    def limpiar_busqueda():
        st.session_state['empresa_seleccionada'] = None
        
    boton_ranking = st.button("🔄 Generar Ranking Completo", type="primary", use_container_width=True, on_click=limpiar_busqueda)

with col_der:
    st.subheader("Buscador Específico")
    st.write("Busca por nombre o ticker (Ej: Amadeus, Amazon...)")
    
    with st.form(key='search_form'):
        c_input, c_btn = st.columns([4, 1])
        texto_input = c_input.text_input("Empresa", placeholder="Ej: Amazon").strip()
        boton_buscar = c_btn.form_submit_button("🔍 Buscar")
        
        # SI PULSAMOS BUSCAR, GUARDAMOS EN MEMORIA
        if boton_buscar and texto_input:
            st.session_state['empresa_seleccionada'] = texto_input

st.markdown("---")

# ==============================================================================
# 🕵️‍♂️ LÓGICA DEL BUSCADOR ESPECÍFICO (USANDO MEMORIA)
# ==============================================================================
# Ahora preguntamos a la MEMORIA, no al botón
if st.session_state['empresa_seleccionada']:
    
    texto_a_buscar = st.session_state['empresa_seleccionada']
    
    ticker_encontrado = datos.encontrar_ticker(texto_a_buscar)
    nombre_bonito = datos.NOMBRES.get(ticker_encontrado, ticker_encontrado)
    
    st.header(f"🔎 Informe Financiero: {nombre_bonito}")
    
    with st.spinner(f"Redactando informe para {nombre_bonito}..."):
        
        # A) Datos
        df_hist = datos.descargar_datos([ticker_encontrado])
        
        # Verificación crítica
        if df_hist.empty:
            st.error(f"❌ Error: No se han podido descargar datos para '{ticker_encontrado}'.")
            # Importante: No usamos st.stop() aquí para no romper la app, solo avisamos
        else:
            # B) Análisis (Solo si hay datos)
            nota_num, desglose = analisis_fundamental.analizar_calidad_fundamental(ticker_encontrado)
            estado_tec, mensaje_tec, precio, vol = calculos.analizar_semaforo(df_hist, ticker_encontrado)
            
            # C) Conversión a Euros
            if not ticker_encontrado.endswith(".MC"):
                factor_eur = datos.obtener_precio_dolar()
                precio_final = precio * factor_eur
                moneda_origen = "USD"
            else:
                precio_final = precio
                moneda_origen = "EUR"

            # --- LÓGICA DE COLOR UNIFICADA ---
            if estado_tec == "ROJO":
                color_nota = "red"
            elif estado_tec == "NARANJA":
                color_nota = "orange"
            else:
                if nota_num >= 8: color_nota = "green"
                elif nota_num >= 5: color_nota = "orange"
                else: color_nota = "red"

            # --- VISUALIZACIÓN ---
            
            # 1. TARJETAS SUPERIORES
            c1, c2, c3 = st.columns(3)
            c1.metric("Empresa", nombre_bonito)
            c2.metric("Precio Actual (Convertido)", f"{precio_final:.2f} €", delta=f"Origen: {moneda_origen}")
            
            c3.markdown(f"""
                <div style='text-align: center; border: 2px solid {color_nota}; border-radius: 10px; padding: 5px; background-color: rgba(255,255,255,0.05);'>
                    <p style='margin:0; font-size: 14px;'>Calificación Global</p>
                    <h1 style='color: {color_nota}; margin:0; font-size: 40px;'>{nota_num}/10</h1>
                </div>
            """, unsafe_allow_html=True)

            st.divider()
            
            # 2. GRÁFICO Y TEXTO
            gc1, gc2 = st.columns([2, 1])
            with gc1:
                st.subheader("📈 Evolución (1 Año)")
                try:
                    fig = graficos.crear_grafico_lineas(df_hist)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error gráfico: {e}")
            
            with gc2:
                st.subheader("📝 Análisis del Experto IA")
                
                txt_tecnico = f"**Técnicamente**, la acción presenta una tendencia **{estado_tec}**. {mensaje_tec}. "
                if vol > 0.025:
                    txt_tecnico += f"⚠️ Atención a su **alta volatilidad** ({vol*100:.1f}%), riesgo elevado."
                else:
                    txt_tecnico += f"Muestra una volatilidad estable ({vol*100:.1f}%)."

                txt_fund = f"\n\n**Fundamentalmente**, la solidez es de **{nota_num}/10**."
                
                if "✅" in desglose.get("Rentabilidad", ""): txt_fund += " Destaca por su alta Rentabilidad."
                elif "❌" in desglose.get("Rentabilidad", ""): txt_fund += " Preocupa que está en pérdidas."
                if "⚠️" in desglose.get("Valoración (PER)", ""): txt_fund += " El precio parece caro."
                if "💰" in desglose.get("Dividendos", ""): txt_fund += " Paga buenos dividendos."

                if color_nota == "green": conclusion = "🏆 **OPORTUNIDAD CLARA.** Compra recomendada."
                elif color_nota == "orange": conclusion = "⚠️ **PRECAUCIÓN.**"
                else:
                    if estado_tec == "ROJO": conclusion = "⛔ **NO COMPRAR.** Tendencia bajista."
                    else: conclusion = "❌ **NO RECOMENDADA.** Fundamentales débiles."

                st.markdown(txt_tecnico + txt_fund)
                
                if color_nota == "green": st.success(conclusion)
                elif color_nota == "orange": st.warning(conclusion)
                else: st.error(conclusion)

                st.markdown("---")
                st.caption("📋 Desglose de Fundamental:")
                df_tabla = pd.DataFrame(list(desglose.items()), columns=["Indicador", "Evaluación"])
                st.table(df_tabla)


# ==============================================================================
# 🔄 LÓGICA DEL RANKING GENERAL
# ==============================================================================
elif boton_ranking:
    st.info("📡 Escaneando mercados de España y EEUU (Descarga Segura)...")
    
    try:
        df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
        factor_eur = datos.obtener_precio_dolar()
    except Exception as e:
        st.error(f"Error grave descargando datos: {e}"); st.stop()
    
    candidatos = []; lista_roja = []
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
    barra.empty()
    
    if candidatos:
        st.info(f"🔬 Auditando a {len(candidatos)} empresas...")
        verdes, naranjas = [], []
        barra2 = st.progress(0)
        
        for i, item in enumerate(candidatos):
            barra2.progress((i+1)/len(candidatos))
            try:
                nota, desglose = analisis_fundamental.analizar_calidad_fundamental(item["Ticker"])
                item["Nota"] = f"{nota}/10"
                item["Puntuacion"] = nota
                item["Precio"] = f"{item['Precio']:.2f} €"
                item.update(desglose)
                
                if item["Estado"] == "VERDE":
                    if nota >= 5: verdes.append(item)
                    else: item["Motivo"] = "Fundamentales débiles"; naranjas.append(item)
                else: naranjas.append(item)
            except: pass
        barra2.empty()
        
        verdes.sort(key=lambda x: x["Puntuacion"], reverse=True)
        naranjas.sort(key=lambda x: x["Puntuacion"], reverse=True)
        
        def mostrar(lista, n):
            if not lista: st.write("Sin datos.")
            else: 
                cols = ["Empresa", "Precio", "Nota", "Valoración (PER)", "Deuda", "Rentabilidad", "Crecimiento"]
                st.dataframe(pd.DataFrame(lista[:n])[cols], use_container_width=True, hide_index=True)

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
    if lista_roja: st.dataframe(pd.DataFrame(lista_roja)[["Empresa", "Motivo"]], use_container_width=True, hide_index=True)

