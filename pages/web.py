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
# AÑADE ESTO AL FINAL DE TU ARCHIVO web.py
# ---------------------------------------------------------

st.divider()
st.header("📡 Radar de Oportunidades (Scanner)")
st.markdown("Este radar analiza tu lista de vigilancia y detecta qué acciones tienen **mayor potencial de subida** según el consenso de analistas.")

# 1. TU LISTA DE VIGILANCIA
# Puedes añadir o quitar las que quieras (usa los tickers reales)
mis_acciones = ["TSLA", "AAPL", "AMZN", "MSFT", "GOOGL", "NVDA", "NFLX", "META", "AMD", "KO", "MCD", "DIS"]

if st.button("🔄 Escanear Mercado en busca de 'Chollos'"):
    
    lista_oportunidades = []
    
    # Barra de progreso visual
    barra = st.progress(0)
    
    with st.status("Analizando mercado...", expanded=True) as status:
        for i, ticker in enumerate(mis_acciones):
            try:
                # Descargamos datos
                stock = yf.Ticker(ticker)
                info = stock.info
                
                nombre = info.get('shortName', ticker)
                precio_actual = info.get('currentPrice', 0)
                precio_objetivo = info.get('targetMeanPrice', 0) # Precio que estiman los analistas
                
                # Calculamos el POTENCIAL DE SUBIDA
                # (Cuánto le falta para llegar al precio objetivo)
                if precio_actual > 0 and precio_objetivo > 0:
                    potencial = ((precio_objetivo - precio_actual) / precio_actual) * 100
                    
                    # Guardamos los datos
                    lista_oportunidades.append({
                        "Empresa": nombre,
                        "Ticker": ticker,
                        "Precio": f"${precio_actual}",
                        "Objetivo": f"${precio_objetivo}",
                        "Potencial": potencial  # Guardamos el número limpio para ordenar después
                    })
                    
                status.write(f"✅ Analizada: {ticker}")
                
            except Exception as e:
                status.write(f"❌ Error con {ticker}")
            
            # Actualizamos la barra de progreso
            barra.progress((i + 1) / len(mis_acciones))

        status.update(label="¡Escaneo completado!", state="complete")

    # 2. PROCESAR Y ORDENAR RESULTADOS
    if lista_oportunidades:
        # Ordenamos la lista: Las que tienen MAYOR potencial primero
        lista_ordenada = sorted(lista_oportunidades, key=lambda x: x['Potencial'], reverse=True)
        
        # 3. MOSTRAR EL "TOP 3" GANADOR
        st.subheader("🏆 Top 3 Oportunidades de Compra (Según Analistas)")
        
        top_3 = lista_ordenada[:3]
        
        cols = st.columns(3)
        for i, accion in enumerate(top_3):
            color = "green" if accion['Potencial'] > 0 else "red"
            cols[i].markdown(f"### {i+1}. {accion['Empresa']}")
            cols[i].metric(
                label="Potencial de Subida", 
                value=f"{accion['Potencial']:.2f}%", 
                delta_color="normal"
            )
            cols[i].write(f"Precio actual: **{accion['Precio']}**")
            cols[i].write(f"Debería valer: **{accion['Objetivo']}**")

        # 4. LA IA DA SU VEREDICTO FINAL
        st.divider()
        st.write("🤖 **El Consultor IA está revisando estas oportunidades...**")
        
        datos_para_ia = str(top_3) # Le pasamos los datos brutos de las 3 mejores
        
        prompt_radar = f"""
        Actúa como un gestor de fondos agresivo. Acabo de escanear el mercado y estas son las 3 acciones con mayor descuento (mayor diferencia entre precio actual y precio objetivo):
        
        {datos_para_ia}
        
        Dime:
        1. ¿Cuál de las 3 te parece la oportunidad más clara y por qué?
        2. ¿Alguna de ellas podría ser una "trampa" (que esté barata porque la empresa va mal)?
        3. Define un precio de entrada agresivo para la mejor opción.
        """
        
        try:
            consejo = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt_radar,
            )
            st.info(consejo.text)
        except:
            st.error("La IA está descansando, pero los datos de arriba son correctos.")
            
    else:
        st.warning("No se pudieron obtener datos suficientes.")
