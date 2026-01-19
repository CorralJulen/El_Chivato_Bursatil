import yfinance as yf

def obtener_datos_fundamentales(ticker):
    """Descarga la ficha técnica de la empresa."""
    try:
        empresa = yf.Ticker(ticker)
        return empresa.info
    except:
        return None

def analizar_calidad_fundamental(ticker):
    """
    Analiza la empresa y devuelve una NOTA y un DESGLOSE por columnas.
    """
    info = obtener_datos_fundamentales(ticker)
    
    # Valores por defecto (guiones) por si no hay datos
    desglose = {
        "Valoración (PER)": "⚪ N/A",
        "Deuda": "⚪ N/A",
        "Rentabilidad": "⚪ N/A",
        "Dividendos": "⚪ No paga",
        "Crecimiento": "⚪ Estancada"
    }

    if not info:
        return 0, desglose

    nota = 0

    # --- 1. VALORACIÓN (PER) ---
    per = info.get('trailingPE', None)
    if per:
        if per < 25:
            nota += 2
            desglose["Valoración (PER)"] = f"✅ Buena ({per:.1f})"
        elif per > 50:
            nota -= 1
            desglose["Valoración (PER)"] = f"⚠️ Cara ({per:.1f})"
        else:
            desglose["Valoración (PER)"] = f"⚖️ Normal ({per:.1f})"
    
    # --- 2. DEUDA (Debt/Equity) ---
    deuda = info.get('debtToEquity', None)
    if deuda:
        if deuda < 150: # Menos de 1.5 veces
            nota += 2
            desglose["Deuda"] = "✅ Baja"
        else:
            nota -= 2
            desglose["Deuda"] = "⚠️ Alta"

    # --- 3. RENTABILIDAD (Márgenes) ---
    margen = info.get('profitMargins', 0)
    if margen > 0.10:
        nota += 2
        desglose["Rentabilidad"] = f"✅ Alta ({margen*100:.0f}%)"
    elif margen > 0:
        nota += 1
        desglose["Rentabilidad"] = f"⚖️ Normal ({margen*100:.0f}%)"
    else:
        nota -= 3
        desglose["Rentabilidad"] = "❌ Pérdidas"

    # --- 4. DIVIDENDOS ---
    div = info.get('dividendYield', 0)
    if div and div > 0.02:
        nota += 1
        desglose["Dividendos"] = f"💰 Rico ({div*100:.1f}%)"

    # --- 5. CRECIMIENTO ---
    crec = info.get('revenueGrowth', 0)
    if crec > 0.05:
        nota += 1
        desglose["Crecimiento"] = "🚀 Sube"
    elif crec < 0:
        desglose["Crecimiento"] = "📉 Baja"

    # Nota final (0 a 10)
    nota_final = min(10, max(0, nota + 2))
    
    return nota_final, desglose