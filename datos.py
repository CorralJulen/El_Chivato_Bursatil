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
    """Intenta adivinar el Ticker basándose en el nombre."""
    texto = texto_busqueda.strip().upper()
    if texto in EMPRESAS_SELECCIONADAS: return texto
    for ticker, nombre in NOMBRES.items():
        if texto in nombre.upper(): return ticker
    return texto

def descargar_datos(tickers):
    """
    Descarga España y EEUU asegurando que las columnas tengan el nombre del Ticker.
    """
    print(f"📡 Iniciando descarga segura para: {tickers}")
    
    lista_es = [t for t in tickers if ".MC" in t]
    lista_us = [t for t in tickers if ".MC" not in t]
    
    df_final = pd.DataFrame()

    def procesar_descarga(lista):
        if not lista: return pd.DataFrame()
        try:
            # Descargamos
            datos = yf.download(lista, period="1y", progress=False, auto_adjust=True)
            
            # Extraemos solo el cierre ('Close')
            if 'Close' in datos.columns:
                df = datos['Close']
            else:
                df = datos # Por si acaso ya viene directo
            
            # CORRECCIÓN DE COLUMNAS (La parte importante)
            # Si es una Serie (1 sola empresa), la convertimos a DataFrame y le ponemos su nombre
            if isinstance(df, pd.Series):
                df = df.to_frame()
                df.columns = lista # Forzamos que la columna se llame 'BBVA.MC' y no 'Close'
            
            # Si es un DataFrame de 1 sola columna pero se llama 'Close'
            elif isinstance(df, pd.DataFrame) and len(df.columns) == 1 and len(lista) == 1:
                df.columns = lista
                
            return df
        except Exception as e:
            print(f"Error descargando {lista}: {e}")
            return pd.DataFrame()

    # Procesamos ambas listas
    df_es = procesar_descarga(lista_es)
    df_us = procesar_descarga(lista_us)
    
    # Unimos
    if not df_es.empty:
        df_final = pd.concat([df_final, df_es], axis=1)
    if not df_us.empty:
        df_final = pd.concat([df_final, df_us], axis=1)

    # Limpieza de fechas
    if not df_final.empty:
        df_final.index = df_final.index.tz_localize(None)
        
    return df_final

def obtener_precio_dolar():
    """Devuelve cuánto vale 1 Dólar en Euros."""
    try:
        tasa = yf.Ticker("EURUSD=X").history(period="1d")['Close'].iloc[-1]
        return 1 / tasa
    except:
        return 1.0
