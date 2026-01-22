import streamlit as st
from google import genai
import yfinance as yf

# 1. CONFIGURACIÓN VISUAL
st.set_page_config(page_title="Buscador Universal de Bolsa", page_icon="📈")
st.title("📈 Buscador Universal de Inversiones")
st.markdown("Escribe el nombre de **cualquier empresa** y la IA analizará sus datos y su gráfico.")

# 2. CONFIGURACIÓN DE SEGURIDAD (Busca la clave en la "Caja Fuerte")
try:
    # Intenta coger la clave de los secretos de Streamlit
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    # Si no la encuentra (porque estás en tu PC y no has configurado el archivo), avisa
    st.error("⚠️ No he encontrado la API Key. Si estás en local, configura .streamlit/secrets.toml")
    st.stop()

if api_key:
    client = genai.Client(api_key=api_key)

# 3. EL BUSCADOR
nombre_empresa = st.text_input("Nombre de la empresa (Ej: Adidas, Ferrari, Inditex...):")

if st.button("🔍 Buscar y Analizar"):
    if nombre_empresa and api_key:
        try:
            # --- FASE 1: DETECTIVE DE TICKERS ---
            with st.status("🤖 Localizando empresa y descargando gráficos...", expanded=True) as status:
                
                # Preguntamos a Gemini el código
                prompt_ticker = f"""
                Responde SOLO con el símbolo (Ticker) de Yahoo Finance para la empresa: "{nombre_empresa}".
                Si no estás seguro, responde "ERROR".
                """
                
                respuesta_ticker = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt_ticker,
                )
                
                ticker_encontrado = respuesta_ticker.text.strip()
                
                if "ERROR" in ticker_encontrado:
                    st.error(f"No encontré el código para '{nombre_empresa}'.")
                    st.stop()
                
                status.write(f"✅ Empresa localizada: **{ticker_encontrado}**")
                
                # --- FASE 2: DESCARGA DE DATOS Y GRÁFICOS ---
                stock = yf.Ticker(ticker_encontrado)
                info = stock.info
                
                # A) Datos básicos
                precio = info.get('currentPrice', info.get('previousClose', 0))
                per = info.get('trailingPE', 'N/A')
                moneda = info.get('currency', 'EUR')
                
                # B) ¡LA NOVEDAD! Descargamos el historial de 1 año para el gráfico
                historial = stock.history(period="1y")
                
                # C) Noticias
                try:
                    noticias = stock.news[:3]
                    titulares = [n.get('title') for n in noticias]
                except:
                    titulares = ["Sin noticias recientes."]
                
                status.update(label="¡Análisis completado!", state="complete")

            # --- FASE 3: MOSTRAR RESULTADOS VISUALES ---
            st.divider()
            
            # 1. LAS MÉTRICAS
            col1, col2, col3 = st.columns(3)
            col1.metric("Precio Actual", f"{precio} {moneda}")
            col2.metric("PER", per)
            
            # Calculamos cuánto ha subido/bajado en el año para mostrarlo en verde/rojo
            if not historial.empty:
                precio_inicio = historial['Close'].iloc[0]
                variacion = ((precio - precio_inicio) / precio_inicio) * 100
                col3.metric("Variación (1 Año)", f"{variacion:.2f}%")

            # 2. EL GRÁFICO (Aquí está la magia visual)
            st.subheader(f"📉 Evolución del precio: {nombre_empresa}")
            # Pintamos solo la columna 'Close' (Precio de cierre)
            st.line_chart(historial['Close'], color="#00FF00") 

            # 3. EL INFORME DE LA IA
            st.subheader("🤖 Análisis de Inteligencia Artificial")
            
            prompt_analisis = f"""
            Analiza la empresa {nombre_empresa} ({ticker_encontrado}) con estos datos:
            - Precio: {precio} {moneda}
            - PER: {per}
            - Variación anual: {variacion if not historial.empty else 'N/A'}%
            - Últimas noticias: {titulares}

            Redacta un análisis breve:
            1. 📊 **Tendencia:** ¿La variación anual es buena?
            2. 🚦 **Valoración:** ¿Está cara o barata según el PER?
            3. 🎯 **Veredicto:** ¿Comprar, Vender o Mantener?
            """
            
            with st.spinner('Gemini está estudiando el gráfico y las noticias...'):
                analisis = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt_analisis,
                )
                st.info(analisis.text)

        except Exception as e:
            st.error(f"Error: {e}")

    elif not api_key:

        st.warning("⚠️ Falta la API Key.")

            # ---------------------------------------------------------
# ---------------------------------------------------------
# ---------------------------------------------------------

st.divider()
st.header("📡 Radar de Oportunidades Masivo")
st.markdown("Escanea índices completos para encontrar las acciones más infravaloradas según los analistas.")

# 1. SELECTOR DE MERCADO
mercado = st.radio("¿Qué mercado quieres escanear?", ["🇪🇸 IBEX 35 (España)", "🇺🇸 Top 50 Tech & Blue Chips (EEUU)"], horizontal=True)

# 2. DEFINICIÓN DE LISTAS (Los índices)
if "España" in mercado:
    # Lista oficial IBEX 35 (con el sufijo .MC necesario para Yahoo)
    tickers_a_escanear = [
        "ITX.MC", "IBE.MC", "SAN.MC", "BBVA.MC", "TEF.MC", "REP.MC", "CABK.MC", "ACS.MC", 
        "AENA.MC", "AMS.MC", "MTS.MC", "SAB.MC", "FER.MC", "GRF.MC", "IAG.MC", "NTGY.MC", 
        "ANA.MC", "ACX.MC", "ENG.MC", "ELE.MC", "MAP.MC", "BKT.MC", "CLNX.MC", "COL.MC", 
        "LOG.MC", "MER.MC", "MEL.MC", "PHM.MC", "RED.MC", "ROVI.MC", "SOL.MC", "VIS.MC"
    ]
else:
    # Lista Top 50 EEUU (Mezcla de Tech, Salud, Finanzas y Consumo)
    tickers_a_escanear = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK-B", "UNH", "JNJ", 
        "XOM", "V", "JPM", "PG", "MA", "HD", "CVX", "MRK", "ABBV", "PEP", "KO", "LLY", 
        "BAC", "AVGO", "TMO", "COST", "DIS", "MCD", "CSCO", "ABT", "DHR", "ACN", "NFLX", 
        "VZ", "NKE", "CRM", "INTC", "CMCSA", "PFE", "ADBE", "WMT", "AMD", "QCOM", "IBM", 
        "TXN", "HON", "AMGN", "UNP", "LOW", "SPGI"
    ]

# 3. BOTÓN DE ESCANEO
if st.button(f"🔍 Escanear {len(tickers_a_escanear)} empresas ahora"):
    
    lista_oportunidades = []
    errores = 0
    
    # Barra de progreso
    barra_progreso = st.progress(0)
    texto_estado = st.empty() # Texto que cambia dinámicamente
    
    # --- INICIO DEL BUCLE DE ANÁLISIS ---
    for i, ticker in enumerate(tickers_a_escanear):
        try:
            # Actualizamos mensaje visual
            texto_estado.text(f"Analizando {i+1}/{len(tickers_a_escanear)}: {ticker}...")
            
            # Descarga de datos
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extraemos datos clave
            precio_actual = info.get('currentPrice', info.get('previousClose', 0))
            precio_objetivo = info.get('targetMeanPrice', 0)
            nombre = info.get('shortName', ticker)
            recomendacion = info.get('recommendationKey', 'none').upper() # buy, hold, sell
            
            # FILTRO DE CALIDAD: Solo guardamos si tenemos ambos precios
            if precio_actual > 0 and precio_objetivo > 0:
                potencial = ((precio_objetivo - precio_actual) / precio_actual) * 100
                
                lista_oportunidades.append({
                    "Ticker": ticker,
                    "Empresa": nombre,
                    "Precio": precio_actual,
                    "Objetivo": precio_objetivo,
                    "Potencial %": round(potencial, 2),
                    "Recomendación": recomendacion
                })
            
        except Exception as e:
            errores += 1
        
        # Actualizar barra (matemática simple: índice actual / total)
        barra_progreso.progress((i + 1) / len(tickers_a_escanear))

    texto_estado.text("¡Análisis finalizado!")
    st.success(f"Escaneadas {len(tickers_a_escanear)} empresas. Detectadas {len(lista_oportunidades)} con datos válidos.")

    # --- RESULTADOS ---
    if lista_oportunidades:
        # Ordenamos: Las de mayor potencial arriba
        df_resultados = sorted(lista_oportunidades, key=lambda x: x['Potencial %'], reverse=True)
        
        # 1. MOSTRAMOS EL TOP 5 GANADOR
        st.subheader("🏆 Top 5: Mayores Oportunidades de Compra")
        
        cols = st.columns(5)
        for i in range(min(5, len(df_resultados))):
            empresa = df_resultados[i]
            with cols[i]:
                # Ponemos color verde si el potencial es positivo
                color = "green" if empresa['Potencial %'] > 0 else "red"
                st.markdown(f"**{i+1}. {empresa['Ticker']}**")
                st.write(f"_{empresa['Empresa'][:15]}..._") # Cortamos el nombre si es muy largo
                st.metric(label="Potencial", value=f"{empresa['Potencial %']}%", delta_color="normal")
                st.caption(f"Recom: {empresa['Recomendación']}")

        # 2. TABLA COMPLETA (Para que el usuario vea todo)
        st.divider()
        with st.expander("📊 Ver tabla completa de resultados"):
            st.dataframe(df_resultados)

       # 3. LA IA ANALIZA AL GANADOR
        ganador = df_resultados[0]
        st.divider()
        st.write(f"🤖 **La IA está analizando la oportunidad Nº1: {ganador['Empresa']}...**")
        
        prompt_auto = f"""
        Actúa como inversor experto. Acabo de hacer un escáner de mercado y la empresa con MAYOR descuento es:
        {ganador['Empresa']} ({ganador['Ticker']}).
        - Precio Actual: {ganador['Precio']}
        - Precio Objetivo Analistas: {ganador['Objetivo']}
        - Potencial de subida: {ganador['Potencial %']}%
        - Recomendación consenso: {ganador['Recomendación']}

        Dime en 3 puntos breves:
        1. ¿Por qué crees que el mercado la ha castigado tanto (por qué está barata)?
        2. ¿Es una oportunidad real o un "cuchillo cayendo" (riesgo de quiebra)?
        3. Estrategia: ¿Entrarías ya o esperarías?
        """
        
        try:
            with st.spinner("Consultando a Gemini..."):
                analisis = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt_auto,
                )
                st.info(analisis.text)
        except Exception as e:
            st.error(f"Error detallado de la IA: {e}")
