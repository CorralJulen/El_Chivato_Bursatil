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
    Descarga España y EEUU por separado para evitar fallos.
    Devuelve precios en moneda original (la conversión se hace fuera).
    """
    print(f"📡 Iniciando descarga segura...")
    
    # 1. Separamos listas
    lista_es = [t for t in tickers if ".MC" in t]
    lista_us = [t for t in tickers if ".MC" not in t]
    
    df_final = pd.DataFrame()

    # 2. Descargar España
    if lista_es:
        try:
            df_es = yf.download(lista_es, period="1y", progress=False, auto_adjust=True)['Close']
            # Corrección si solo es 1 empresa
            if isinstance(df_es, pd.Series): df_es = df_es.to_frame()
            df_final = pd.concat([df_final, df_es], axis=1)
        except: pass

    # 3. Descargar EEUU
    if lista_us:
        try:
            df_us = yf.download(lista_us, period="1y", progress=False, auto_adjust=True)['Close']
            if isinstance(df_us, pd.Series): df_us = df_us.to_frame()
            df_final = pd.concat([df_final, df_us], axis=1)
        except: pass
        
    # Limpieza de fechas (quitar hora)
    if not df_final.empty:
        df_final.index = df_final.index.tz_localize(None)
        
    return df_final

def obtener_precio_dolar():
    """Devuelve cuánto vale 1 Dólar en Euros."""
    try:
        tasa = yf.Ticker("EURUSD=X").history(period="1d")['Close'].iloc[-1]
        return 1 / tasa
    except:
        return 1.0 # Si falla, 1 a 1