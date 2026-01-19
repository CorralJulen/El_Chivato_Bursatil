import streamlit as st
import pandas as pd
import datos
import calculos
import analisis_fundamental
import graficos

st.set_page_config(page_title="Semáforo Pro", page_icon="🚦", layout="wide")
st.title("🚦 Semáforo & Analizador Pro")

# --- 1. GESTIÓN DE MEMORIA ---
if 'busqueda_activa' not in st.session_state:
    st.session_state['busqueda_activa'] = None

def activar_ranking():
    st.session_state['busqueda_activa'] = None

# --- 2. BOTONERA SUPERIOR ---
st.markdown("---")
col_izq, col_der = st.columns([2, 3])

with col_izq:
    st.subheader("Escáner General")
    st.write("Analiza las 60 empresas vigiladas.")
    boton_ranking = st.button("🔄 Generar Ranking Completo", type="primary", use_container_width=True, on_click=activar_ranking)

with col_der:
    st.subheader("Buscador Específico")
    st.write("Busca por nombre o ticker (Ej: Amadeus, Amazon...)")
    c1, c2 = st.columns([3, 1])
    texto_input = c1.text_input("Empresa", placeholder="Ej: Inditex", label_visibility="collapsed")
    if c2.button("🔍 Buscar"):
        if texto_input:
            st.session_state['busqueda_activa'] = texto_input
        else:
            st.warning("Escribe algo primero.")

st.markdown("---")

# ==============================================================================
# ESCENARIO A: BÚSQUEDA INDIVIDUAL (Esto ya funcionaba)
# ==============================================================================
if st.session_state['busqueda_activa']:
    texto_a_buscar = st.session_state['busqueda_activa']
    ticker_encontrado = datos.encontrar_ticker(texto_a_buscar)
    nombre_bonito = datos.NOMBRES.get(ticker_encontrado, ticker_encontrado)
    
    st.header(f"🔎 Informe: {nombre_bonito}")
    
    with st.spinner("Analizando mercado..."):
        df_hist = datos.descargar_datos([ticker_encontrado])
        
    if df_hist.empty:
        st.error(f"❌ No he encontrado datos para '{ticker_encontrado}'.")
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
            elif estado_tec == "NARANJA": color_nota = "orange"

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
                try:
                    fig = graficos.crear_grafico_lineas(df_hist)
                    st.pyplot(fig)
                except: st.warning("Gráfico no disponible")
            with t_col:
                st.write(f"**Tendencia:** {estado_tec}")
                if color_nota == "green": st.success("✅ COMPRA")
                elif color_nota == "orange": st.warning("⚠️ PRECAUCIÓN")
                else: st.error("⛔ NO INVERTIR")
                st.dataframe(pd.DataFrame(list(desglose.items()), columns=["Ratio", "Estado"]), hide_index=True)
        except Exception as e:
            st.error(f"Error al procesar: {e}")

# ==============================================================================
# ESCENARIO B: RANKING GENERAL (MODO RESILIENTE 🛡️)
# ==============================================================================
elif boton_ranking:
    st.info("📡 Fase 1: Descargando Precios (España y EEUU)...")
    
    try:
        df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
        factor_eur = datos.obtener_precio_dolar()
    except Exception as e:
        st.error(f"Error descarga masiva: {e}"); st.stop()
    
    lista_preliminar = []
    barra = st.progress(0)
    
    # 1. ANÁLISIS TÉCNICO (RÁPIDO)
    for i, ticker in enumerate(datos.EMPRESAS_SELECCIONADAS):
        barra.progress((i + 1) / len(datos.EMPRESAS_SELECCIONADAS))
        try:
            estado, mensaje, precio, vol = calculos.analizar_semaforo(df_todos, ticker)
            precio_final = precio * factor_eur if not ticker.endswith(".MC") else precio
            
            # Guardamos todo lo que encontremos, aunque sea solo precio
            lista_preliminar.append({
                "Ticker": ticker,
                "Empresa": datos.NOMBRES.get(ticker, ticker),
                "Precio": precio_final,
                "Estado": estado,
                "Motivo": mensaje
            })
        except: pass
    barra.empty()
    
    # 2. ANÁLISIS FUNDAMENTAL (LENTO Y PROPENSO A FALLOS)
    if lista_preliminar:
        st.info(f"🔬 Fase 2: Auditando {len(lista_preliminar)} empresas... (Esto puede tardar)")
        
        candidatos_finales = []
        barra2 = st.progress(0)
        
        for i, item in enumerate(lista_preliminar):
            barra2.progress((i+1)/len(lista_preliminar))
            
            # Valores por defecto por si falla Yahoo
            nota = 0
            desglose = {"Error": "Datos no disponibles"}
            
            # Intentamos descargar fundamental
            try:
                # Solo analizamos fundamental si la empresa no dio error técnico
                if item["Estado"] != "ERROR":
                    nota, desglose = analisis_fundamental.analizar_calidad_fundamental(item["Ticker"])
            except:
                # Si falla, no rompemos el bucle, simplemente le ponemos nota baja
                item["Motivo"] += " (Fallo datos fundamental)"
            
            # Asignamos datos (o los por defecto si falló)
            item["Nota"] = f"{nota}/10"
            item["Puntuacion"] = nota
            item["Precio"] = f"{item['Precio']:.2f} €"
            item.update(desglose)
            
            candidatos_finales.append(item)
            
        barra2.empty()
        
        # Clasificación
        verdes = [x for x in candidatos_finales if x["Estado"] == "VERDE" and x["Puntuacion"] >= 5]
        naranjas = [x for x in candidatos_finales if x not in verdes and x["Estado"] != "ROJO" and x["Estado"] != "ERROR"]
        rojas = [x for x in candidatos_finales if x["Estado"] == "ROJO"]

        # Ordenar
        verdes.sort(key=lambda x: x["Puntuacion"], reverse=True)
        naranjas.sort(key=lambda x: x["Puntuacion"], reverse=True)

        # FUNCIÓN PARA MOSTRAR TABLA SEGURA
        def pintar_tabla_segura(lista_datos):
            if not lista_datos:
                st.write("No hay resultados en esta categoría.")
                return
            
            # Convertimos a DataFrame
            df = pd.DataFrame(lista_datos)
            
            # Columnas deseables
            cols_deseadas = ["Empresa", "Precio", "Nota", "Valoración (PER)", "Rentabilidad", "Dividendos", "Deuda", "Motivo"]
            
            # Filtramos: Solo mostramos las columnas que REALMENTE EXISTEN en los datos
            # (Así si falla 'Dividendos' no explota la tabla, simplemente no sale esa columna)
            cols_reales = [c for c in cols_deseadas if c in df.columns]
            
            st.dataframe(df[cols_reales], use_container_width=True, hide_index=True)

        # --- RESULTADOS ---
        st.success(f"🟢 OPORTUNIDADES ({len(verdes)})")
        if verdes:
            t1, t2 = st.tabs(["Top 5", "Lista Completa"])
            with t1: pintar_tabla_segura(verdes[:5])
            with t2: pintar_tabla_segura(verdes)
            
        st.warning(f"🟠 MIXTO / PRECAUCIÓN ({len(naranjas)})")
        if naranjas:
            t3, t4 = st.tabs(["Top 5", "Lista Completa"])
            with t3: pintar_tabla_segura(naranjas[:5])
            with t4: pintar_tabla_segura(naranjas)
            
        st.error(f"❌ EVITAR ({len(rojas)})")
        if rojas:
            pintar_tabla_segura(rojas)

    else:
        st.warning("No se pudieron obtener datos técnicos de ninguna empresa.")





