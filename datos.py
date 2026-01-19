import yfinance as yf
import pandas as pd

# --- DICCIONARIO DE NOMBRES ---
NOMBRES = {
    # === ESPAÑA (IBEX 35) ===
    'BBVA.MC': 'BBVA', 'SAN.MC': 'Banco Santander', 'ITX.MC': 'Inditex (Zara)',
    'TEF.MC': 'Telefónica', 'IBE.MC': 'Iberdrola', 'REP.MC': 'Repsol',
    'AENA.MC': 'Aena', 'AMS.MC': 'Amadeus', 'FER.MC': 'Ferrovial',
    'ACS.MC': 'ACS', 'GRF.MC': 'Grifols', 'CLNX.MC': 'Cellnex',
    'ENG.MC': 'Enagás', 'ELE.MC': 'Endesa', 'MAP.MC': 'Mapfre',
    'SAB.MC': 'Banco Sabadell', 'BKT.MC': 'Bankinter', 'ACX.MC': 'Acerinox',
    'MTS.MC': 'ArcelorMittal', 'IAG.MC': 'IAG (Iberia)', 'NTGY.MC': 'Naturgy',
    'RED.MC': 'Red Eléctrica', 'COL.MC': 'Colonial', 'MER.MC': 'Merlin Properties',
    'ANA.MC': 'Acciona', 'ANE.MC': 'Acciona Energía', 'LOG.MC': 'Logista',
    'ROVI.MC': 'Rovi', 'SCYR.MC': 'Sacyr', 'SLR.MC': 'Solaria',
    'UNI.MC': 'Unicaja', 'FDR.MC': 'Fluidra', 'MEL.MC': 'Meliá Hoteles',

    # === EEUU (WALL STREET) ===
    'AAPL': 'Apple', 'MSFT': 'Microsoft', 'GOOGL': 'Google (Alphabet)',
    'AMZN': 'Amazon', 'TSLA': 'Tesla', 'META': 'Meta (Facebook)',
    'NVDA': 'Nvidia', 'NFLX': 'Netflix', 'AMD': 'AMD', 'INTC': 'Intel',
    'KO': 'Coca-Cola', 'PEP': 'PepsiCo', 'MCD': "McDonald's", 'DIS': 'Disney',
    'NKE': 'Nike', 'SBUX': 'Starbucks', 'WMT': 'Walmart', 'JPM': 'JP Morgan',
    'V': 'Visa', 'MA': 'Mastercard', 'BRK-B': 'Berkshire Hathaway',
    'CRM': 'Salesforce', 'ADBE': 'Adobe', 'PYPL': 'PayPal'
}

EMPRESAS_SELECCIONADAS = list(NOMBRES.keys())

def encontrar_ticker(texto_busqueda):
    texto = texto_busqueda.strip().upper()
    if texto in EMPRESAS_SELECCIONADAS: return texto
    for ticker, nombre in NOMBRES.items():
        if texto in nombre.upper(): return ticker
    return texto

def descargar_datos(tickers):
    """
    Descarga robusta que maneja Series, DataFrames y MultiIndex.
    """
    if not tickers: return pd.DataFrame()
    
    print(f"📡 Descargando: {tickers}")
    
    # Separamos listas para evitar conflictos de moneda/mercado
    lista_es = [t for t in tickers if ".MC" in t]
    lista_us = [t for t in tickers if ".MC" not in t]
    
    df_final = pd.DataFrame()

    def procesar(lista_tickers):
        if not lista_tickers: return pd.DataFrame()
        try:
            # Forzamos descarga como grupo
            datos = yf.download(lista_tickers, period="1y", auto_adjust=True, progress=False)
            
            # Caso 1: Yahoo devuelve MultiIndex (Price, Ticker)
            if isinstance(datos.columns, pd.MultiIndex):
                try:
                    df = datos['Close'] # Intentamos coger solo cierre
                except KeyError:
                    # Si falla, a veces la columna se llama diferente o no hay MultiIndex claro
                    df = datos
            # Caso 2: Index simple (Open, Close, etc.) - Típico de 1 sola empresa
            elif 'Close' in datos.columns:
                df = datos[['Close']] # Lo mantenemos como DataFrame
            else:
                df = datos # Fallback
            
            # --- LIMPIEZA CRÍTICA ---
            # Si descargamos 1 sola empresa, Yahoo a veces no pone el nombre del Ticker en la columna.
            # Aquí lo forzamos manualmente.
            if len(lista_tickers) == 1:
                # Si es una Serie, la convertimos
                if isinstance(df, pd.Series):
                    df = df.to_frame()
                
                # Si tiene 1 columna, le ponemos el nombre del ticker SÍ o SÍ.
                if df.shape[1] == 1:
                    df.columns = lista_tickers
                    
            return df
        except Exception as e:
            print(f"⚠️ Error en descarga parcial {lista_tickers}: {e}")
            return pd.DataFrame()

    # Ejecutamos
    df_es = procesar(lista_es)
    df_us = procesar(lista_us)
    
    # Unimos
    if not df_es.empty:
        df_final = pd.concat([df_final, df_es], axis=1)
    if not df_us.empty:
        df_final = pd.concat([df_final, df_us], axis=1)
        
    # Limpiar Zona Horaria (Causa común de fallos en gráficos)
    if not df_final.empty:
        df_final.index = df_final.index.tz_localize(None)
        
    return df_final

def obtener_precio_dolar():
    try:
        tasa = yf.Ticker("EURUSD=X").history(period="1d")['Close'].iloc[-1]
        return 1 / tasa
    except:
        return 1.0
        return 1 / tasa
    except:
        return 1.0

