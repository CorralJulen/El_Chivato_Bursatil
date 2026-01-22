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