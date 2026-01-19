import pandas as pd
import numpy as np

def calcular_retornos_diarios(df):
    return df.pct_change().dropna()

def calcular_riesgo(retornos):
    return retornos.std()

def calcular_retorno_acumulado(df):
    if df.empty: return 0
    return (df.iloc[-1] - df.iloc[0]) / df.iloc[0]

def analizar_semaforo(df, ticker):
    """Analiza tendencia y volatilidad."""
    if ticker not in df.columns:
        return "ERROR", "No hay datos", 0, 0
    
    serie = df[ticker].dropna()
    
    if serie.empty:
        return "ERROR", "Serie vacía", 0, 0
        
    # Variables clave
    precio_actual = serie.iloc[-1]
    media_50 = serie.rolling(window=50).mean().iloc[-1]
    
    # Volatilidad (últimos 30 días)
    retornos = serie.pct_change().tail(30)
    volatilidad = retornos.std()
    
    # Si falta la media (acción muy nueva), usamos precio vs ayer
    if pd.isna(media_50):
        media_50 = precio_actual # Parche para no romper
    
    # REGLAS DEL JUEZ
    # Nota: El análisis de tendencia sirve igual en Dólares que en Euros
    if precio_actual < media_50:
        estado = "ROJO"
        mensaje = "Tendencia Bajista"
    elif precio_actual > media_50 and volatilidad > 0.015:
        estado = "NARANJA"
        mensaje = "Alta Volatilidad"
    else:
        estado = "VERDE"
        mensaje = "Tendencia Alcista"
        
    return estado, mensaje, precio_actual, volatilidad