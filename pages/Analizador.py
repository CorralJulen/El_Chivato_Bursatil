import streamlit as st
import pandas as pd
import datos
import calculos
import analisis_fundamental
import graficos

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Analizador Pro", page_icon="📊", layout="wide")

# ==============================================================================
# 🎨 ESTILOS CSS (ESTÉTICA APP FINTECH)
# ==============================================================================
st.markdown("""
<style>
    /* Fondo General */
    .stApp { background-color: #F8F9FA; }
    
    /* Tarjetas Blancas (Contenedores) */
    .css-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #E9ECEF;
        margin-bottom: 15px;
    }
    
    /* Títulos */
    h1, h2, h3 { color: #1A1A1A; font-family: 'Inter', sans-serif; }
    
    /* Botones Estilizados */
    div.stButton > button { border-radius: 6px; font-weight: 600; border: none; }
    div.stButton > button:first-child { background-color: #2C3E50; color: white; }
    div.stButton > button:first-child:hover { background-color: #1A252F; }
    
    /* Métricas Grandes */
    div[data-testid="stMetricValue"] { color: #2E86C1; }
</style>
""", unsafe_allow_html=True)

# --- 1. GESTIÓN DE MEMORIA ---
if 'busqueda_activa' not in st.session_state:
    st.session_state['busqueda_activa'] = None

def activar_ranking():
    st.session_state['busqueda_activa'] = None

# ==============================================================================
# 🏦 CABECERA Y PANEL DE CONTROL
# ==============================================================================
st.title("📊 Terminal de Análisis Bursátil")
st.caption("Inteligencia de Mercado • Datos en Tiempo Real")

st.markdown("---")

# ENVOLTORIO VISUAL (Caja Blanca)
with st.container():
    st.markdown("<div style='background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
    
    col_izq, col_der = st.columns([2, 3])

    with col_izq:
        st.subheader("📡 Escáner General")
        st.write("Analiza las 60 empresas vigiladas.")
        # Botón Ranking
        boton_ranking = st.button("🔄 Generar Ranking Completo", type="primary", use_container_width=True, on_click=activar_ranking)

    with col_der:
        st.subheader("🔎 Buscador Específico")
        st.write("Busca por nombre o ticker (Ej: Amadeus, Amazon...)")
        
        c1, c2 = st.columns([3, 1])
        # Input y Botón
        texto_input = c1.text_input("Empresa", placeholder="Ej: Inditex", label_visibility="collapsed")
        if c2.button("BUSCAR", use_container_width=True):
            if texto_input:
                st.session_state['busqueda_activa'] = texto_input
            else:
                st.warning("Escribe algo primero.")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.write("") # Espacio

# ==============================================================================
# ESCENARIO A: BÚSQUEDA INDIVIDUAL (CON TEXTO IA PRO RESTAURADO)
# ==============================================================================
if st.session_state['busqueda_activa']:
    
    texto_a_buscar = st.session_state['busqueda_activa']
    ticker_encontrado = datos.encontrar_ticker(texto_a_buscar)
    nombre_bonito = datos.NOMBRES.get(ticker_encontrado, ticker_encontrado)
    
    st.header(f"📑 Informe: {nombre_bonito}")
    
    with st.spinner("Analizando mercado a fondo..."):
        df_hist = datos.descargar_datos([ticker_encontrado])
        
    if df_hist.empty:
        st.error(f"❌ No he encontrado datos para '{ticker_encontrado}'.")
    else:
        try:
            # CÁLCULOS
            nota_num, desglose = analisis_fundamental.analizar_calidad_fundamental(ticker_encontrado)
            estado_tec, mensaje_tec, precio, vol = calculos.analizar_semaforo(df_hist, ticker_encontrado)
            
            moneda = "EUR"
            if not ticker_encontrado.endswith(".MC"):
                factor = datos.obtener_precio_dolar()
                precio = precio * factor
                moneda = "USD (Conv)"

            # Colores
            color_nota = "red" 
            if estado_tec == "VERDE":
                if nota_num >= 8: color_nota = "#27AE60" # Verde
                elif nota_num >= 5: color_nota = "#F39C12" # Naranja
                else: color_nota = "#E74C3C" # Rojo
            elif estado_tec == "NARANJA": color_nota = "#F39C12"
            else: color_nota = "#E74C3C"

            # --- VISUALIZACIÓN ---
            with st.container():
                st.markdown("<div style='background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 20px;'>", unsafe_allow_html=True)
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric("Empresa", nombre_bonito)
                kpi2.metric("Precio Actual", f"{precio:.2f} €", delta=moneda)
                
                # Nota con estilo visual
                kpi3.markdown(f"""
                    <div style='text-align: center;'>
                        <span style='font-size: 14px; color: gray;'>Rating IA</span><br>
                        <span style='color: {color_nota}; font-size: 30px; font-weight: bold;'>{nota_num}/10</span>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            g_col, t_col = st.columns([2, 1])
            
            with g_col:
                st.markdown("<div style='background-color: white; padding: 10px; border-radius: 10px; border: 1px solid #eee;'>", unsafe_allow_html=True)
                st.subheader("📈 Gráfico de Precios")
                try:
                    fig = graficos.crear_grafico_lineas(df_hist)
                    st.pyplot(fig)
                except: st.warning("Gráfico no disponible")
                st.markdown("</div>", unsafe_allow_html=True)

            with t_col:
                st.markdown("<div style='background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #eee;'>", unsafe_allow_html=True)
                st.subheader("📝 Análisis del Experto IA")
                
                # --- REDACCIÓN AUTOMÁTICA PRO (RESTAURADA) ---
                txt_tecnico = f"**Técnicamente**, la acción presenta una tendencia **{estado_tec}**. {mensaje_tec}. "
                if vol > 0.025:
                    txt_tecnico += f"⚠️ Atención a su **alta volatilidad** ({vol*100:.1f}%), riesgo elevado."
                else:
                    txt_tecnico += f"Muestra una volatilidad estable ({vol*100:.1f}%)."

                txt_fund = f"\n\n**Fundamentalmente**, la solidez es de **{nota_num}/10**."
                
                # Lógica detallada de texto
                if "✅" in str(desglose.get("Rentabilidad", "")):
                    txt_fund += " Destaca por su alta capacidad de generar beneficios."
                elif "❌" in str(desglose.get("Rentabilidad", "")):
                    txt_fund += " Preocupa que está en pérdidas."
                
                if "⚠️" in str(desglose.get("Valoración (PER)", "")):
                    txt_fund += " El precio parece caro respecto a beneficios."

                if "💰" in str(desglose.get("Dividendos", "")):
                    txt_fund += " Paga dividendos interesantes."

                st.markdown(txt_tecnico + txt_fund)
                
                # Conclusión visual
                if color_nota == "#27AE60":
                    st.success("🏆 **OPORTUNIDAD CLARA.** Compra recomendada.")
                elif color_nota == "#F39C12":
                    st.warning("⚠️ **MANTENER / PRECAUCIÓN.**")
                else:
                    st.error("⛔ **NO INVERTIR AHORA.**")

                st.markdown("---")
                st.caption("Detalles fundamentales:")
                st.dataframe(pd.DataFrame(list(desglose.items()), columns=["Ratio", "Valor"]), hide_index=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error al procesar los datos: {e}")

# ==============================================================================
# ESCENARIO B: RANKING GENERAL (AHORA CON 3 PESTAÑAS)
# ==============================================================================
elif boton_ranking:
    st.info("📡 Escaneando mercados de España y EEUU...")
    
    try:
        df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
        factor_eur = datos.obtener_precio_dolar()
    except Exception as e:
        st.error(f"Error grave: {e}"); st.stop()
    
    candidatos = []; lista_roja = []
    
    # BARRA DE PROGRESO 1
    barra = st.progress(0)
    for i, ticker in enumerate(datos.EMPRESAS_SELECCIONADAS):
        barra.progress((i + 1) / len(datos.EMPRESAS_SELECCIONADAS))
        try:
            estado, mensaje, precio, vol = calculos.analizar_semaforo(df_todos, ticker)
            precio_final = precio * factor_eur if not ticker.endswith(".MC") else precio
            
            item = {
                "Ticker": ticker, "Empresa": datos.NOMBRES.get(ticker, ticker),
                "Precio": precio_final, "Estado": estado, "Motivo": mensaje
            }
            if estado == "ROJO": lista_roja.append(item)
            elif estado != "ERROR": candidatos.append(item) 
        except: pass
    barra.empty()
    
    # FASE 2: FUNDAMENTAL
    if candidatos:
        st.info(f"🔬 Auditando a {len(candidatos)} empresas candidatas...")
        verdes, naranjas = [], []
        
        barra2 = st.progress(0)
        for i, item in enumerate(candidatos):
            barra2.progress((i+1)/len(candidatos))
            try:
                # CÁLCULO SEGURO
                nota, desglose = analisis_fundamental.analizar_calidad_fundamental(item["Ticker"])
                
                item["Nota"] = f"{nota}/10"
                item["Puntuacion"] = nota
                item["Precio"] = f"{item['Precio']:.2f} €"
                item.update(desglose)
                
                if item["Estado"] == "VERDE":
                    if nota >= 5: verdes.append(item)
                    else: item["Motivo"] = "Fundamentales débiles"; naranjas.append(item)
                else: naranjas.append(item)
            except: 
                item["Nota"] = "N/A"; item["Puntuacion"] = 0; naranjas.append(item)

        barra2.empty()
        
        # Ordenamos
        verdes.sort(key=lambda x: x["Puntuacion"], reverse=True)
        naranjas.sort(key=lambda x: x["Puntuacion"], reverse=True)
        
        # FUNCIÓN DE TABLA (ORIGINAL)
        def mostrar_tabla(lista, limite=None):
            if not lista: 
                st.write("Sin datos.")
                return
            df = pd.DataFrame(lista)
            if limite: df = df[:limite]
            
            cols_ver = ["Empresa", "Precio", "Nota", "Valoración (PER)", "Rentabilidad", "Dividendos", "Deuda"]
            cols_finales = [c for c in cols_ver if c in df.columns]
            st.dataframe(df[cols_finales], use_container_width=True, hide_index=True)

        # --- MOSTRAR RESULTADOS (CON 3 TABS) ---
        with st.container():
            st.markdown("<div style='background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #eee;'>", unsafe_allow_html=True)
            
            st.success(f"🟢 OPORTUNIDADES ({len(verdes)})")
            if verdes:
                # AQUÍ ESTÁN LAS 3 PESTAÑAS QUE PEDISTE
                t1, t2, t3 = st.tabs(["Top 5", "Top 10", "Lista Completa"])
                with t1: mostrar_tabla(verdes, 5)
                with t2: mostrar_tabla(verdes, 10)
                with t3: mostrar_tabla(verdes, None) # None = Sin límite
                
            st.warning(f"🟠 RIESGO / MIXTO ({len(naranjas)})")
            if naranjas:
                t4, t5, t6 = st.tabs(["Top 5", "Top 10", "Lista Completa"])
                with t4: mostrar_tabla(naranjas, 5)
                with t5: mostrar_tabla(naranjas, 10)
                with t6: mostrar_tabla(naranjas, None)
                
            st.error(f"❌ EVITAR ({len(lista_roja)})")
            if lista_roja: 
                st.dataframe(pd.DataFrame(lista_roja)[["Empresa", "Motivo"]], use_container_width=True, hide_index=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
