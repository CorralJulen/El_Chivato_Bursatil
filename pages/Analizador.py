import streamlit as st
import pandas as pd
import datos
import calculos
import analisis_fundamental
import graficos

st.set_page_config(page_title="Semáforo Pro", page_icon="🚦", layout="wide")
st.title("🚦 Semáforo & Analizador Pro")

# --- ZONA SUPERIOR ---
st.markdown("---")
col_izq, col_der = st.columns([2, 3])

with col_izq:
    st.subheader("Escáner General")
    st.write("Analiza las 60 empresas vigiladas.")
    boton_ranking = st.button("🔄 Generar Ranking Completo", type="primary", use_container_width=True)

with col_der:
    st.subheader("Buscador Específico")
    st.write("Busca por nombre o ticker (Ej: Amadeus, Amazon...)")
    with st.form(key='search_form'):
        c_input, c_btn = st.columns([4, 1])
        texto_input = c_input.text_input("Empresa", placeholder="Ej: Amazon").strip()
        boton_buscar = c_btn.form_submit_button("🔍 Buscar")

st.markdown("---")

# ==============================================================================
# 🕵️‍♂️ LÓGICA DEL BUSCADOR ESPECÍFICO
# ==============================================================================
if boton_buscar:
    if not texto_input:
        st.warning("Escribe algo para buscar.")
        st.stop()
    
    ticker_encontrado = datos.encontrar_ticker(texto_input)
    nombre_bonito = datos.NOMBRES.get(ticker_encontrado, ticker_encontrado)
    
    st.header(f"🔎 Informe Financiero: {nombre_bonito}")
    
    with st.spinner(f"Redactando informe para {nombre_bonito}..."):
        try:
            # A) Datos
            df_hist = datos.descargar_datos([ticker_encontrado])
            if df_hist.empty:
                st.error(f"No hay datos para '{ticker_encontrado}'.")
                st.stop()

            # B) Análisis
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

            # --- LÓGICA DE COLOR UNIFICADA (LO QUE PEDISTE) ---
            # El color de la caja ahora depende de la tendencia TAMBIÉN.
            if estado_tec == "ROJO":
                color_nota = "red"      # Si cae, alerta roja (aunque sea buena empresa)
            elif estado_tec == "NARANJA":
                color_nota = "orange"   # Si es volátil, precaución
            else:
                # Si es VERDE (sube), entonces miramos la nota fundamental
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
            
            # 2. GRÁFICO (Izquierda) Y TEXTO (Derecha)
            gc1, gc2 = st.columns([2, 1])
            with gc1:
                st.subheader("📈 Evolución (1 Año)")
                fig = graficos.crear_grafico_lineas(df_hist)
                st.pyplot(fig)
            
            with gc2:
                st.subheader("📝 Análisis del Experto IA")
                
                # --- REDACCIÓN AUTOMÁTICA ---
                txt_tecnico = f"**Técnicamente**, la acción presenta una tendencia **{estado_tec}**. {mensaje_tec}. "
                if vol > 0.025:
                    txt_tecnico += f"⚠️ Atención a su **alta volatilidad** ({vol*100:.1f}%), riesgo elevado."
                else:
                    txt_tecnico += f"Muestra una volatilidad estable ({vol*100:.1f}%)."

                txt_fund = f"\n\n**Fundamentalmente**, la solidez es de **{nota_num}/10**."
                
                # Detalles inteligentes
                if "✅" in desglose.get("Rentabilidad", ""):
                    txt_fund += " Destaca por su capacidad de generar beneficios (Alta Rentabilidad)."
                elif "❌" in desglose.get("Rentabilidad", ""):
                    txt_fund += " Preocupa que actualmente está en pérdidas."
                
                if "⚠️" in desglose.get("Valoración (PER)", ""):
                    txt_fund += " El precio parece caro respecto a sus beneficios."

                if "💰" in desglose.get("Dividendos", ""):
                    txt_fund += " Paga dividendos interesantes."

                # Conclusión Coherente con el color
                if color_nota == "green":
                    conclusion = "🏆 **OPORTUNIDAD CLARA.** Tendencia alcista y fundamentales sólidos. Compra recomendada."
                elif color_nota == "orange":
                    conclusion = "⚠️ **MANTENER / PRECAUCIÓN.** Buenos fundamentales pero tendencia dudosa (o viceversa)."
                else: # Red
                    if estado_tec == "ROJO":
                        conclusion = "⛔ **NO COMPRAR AHORA.** Aunque la empresa pueda ser buena, la tendencia es bajista (Cuchillo cayendo)."
                    else:
                        conclusion = "❌ **NO RECOMENDADA.** Los fundamentales son demasiado débiles."

                st.markdown(txt_tecnico + txt_fund)
                
                # Caja de color con la conclusión
                if color_nota == "green":
                    st.success(conclusion)
                elif color_nota == "orange":
                    st.warning(conclusion)
                else:
                    st.error(conclusion)

                # --- TABLA DE INDICADORES ---
                st.markdown("---")
                st.caption("📋 Desglose de Fundamental:")
                df_tabla = pd.DataFrame(list(desglose.items()), columns=["Indicador", "Evaluación"])
                st.table(df_tabla)

        except Exception as e:
            st.error(f"Error analizando la empresa: {e}")

# ==============================================================================
# 🔄 LÓGICA DEL RANKING GENERAL
# ==============================================================================
elif boton_ranking:
    st.info("📡 Escaneando mercados de España y EEUU (Descarga Segura)...")
    
    try:
        # Descarga separada (Gracias al nuevo datos.py)
        df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
        factor_eur = datos.obtener_precio_dolar()
    except Exception as e:
        st.error(f"Error grave: {e}"); st.stop()
    
    candidatos = []; lista_roja = []
    barra = st.progress(0)
    
    # Iteramos sobre la lista completa
    for i, ticker in enumerate(datos.EMPRESAS_SELECCIONADAS):
        barra.progress((i + 1) / len(datos.EMPRESAS_SELECCIONADAS))
        try:
            estado, mensaje, precio, vol = calculos.analizar_semaforo(df_todos, ticker)
            
            # Conversión divisa
            precio_final = precio * factor_eur if not ticker.endswith(".MC") else precio
            
            item = {
                "Ticker": ticker,
                "Empresa": datos.NOMBRES.get(ticker, ticker),
                "Precio": precio_final,
                "Estado": estado,
                "Motivo": mensaje
            }
            
            if estado == "ROJO": lista_roja.append(item)
            elif estado != "ERROR": candidatos.append(item) # Si no es error, es candidato
        except: pass
    barra.empty()
    
    # FASE 2: FUNDAMENTALES
    if candidatos:
        st.info(f"🔬 Auditando a {len(candidatos)} empresas...")
        verdes, naranjas = [], []
        barra2 = st.progress(0)
        
        for i, item in enumerate(candidatos):
            barra2.progress((i+1)/len(candidatos))
            nota, desglose = analisis_fundamental.analizar_calidad_fundamental(item["Ticker"])
            
            item["Nota"] = f"{nota}/10"
            item["Puntuacion"] = nota
            item["Precio"] = f"{item['Precio']:.2f} €"
            item.update(desglose)
            
            if item["Estado"] == "VERDE":
                if nota >= 5: verdes.append(item)
                else: item["Motivo"] = "Fundamentales débiles"; naranjas.append(item)
            else: naranjas.append(item)
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