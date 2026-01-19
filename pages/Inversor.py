import streamlit as st
import pandas as pd
import plotly.express as px
import datos
import calculos
import analisis_fundamental

# --- CONFIGURACIÓN INICIAL ---
# He cambiado también el título de la pestaña del navegador para que cuadre
st.set_page_config(page_title="Gestor Patrimonio IA", page_icon="🏦", layout="wide")

# ==============================================================================
# 🎨 ESTILOS CSS "PREMIUM FINTECH"
# ==============================================================================
st.markdown("""
<style>
    /* 1. FONDO GLOBAL: Gris muy suave */
    .stApp {
        background-color: #F8F9FA;
    }

    /* 2. TARJETAS (Card UI) */
    .css-card {
        background-color: #FFFFFF;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #E9ECEF;
        margin-bottom: 20px;
    }

    /* 3. TÍTULOS */
    h1, h2, h3 {
        color: #1A1A1A;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    /* 4. BOTÓN PRINCIPAL */
    div.stButton > button:first-child {
        background-color: #000000;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: transform 0.2s;
    }
    div.stButton > button:first-child:hover {
        background-color: #333333;
        transform: translateY(-2px);
    }

    /* 5. METRICAS */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #2E86C1;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 🏦 CABECERA TIPO "APP"
# ==============================================================================
c_head1, c_head2 = st.columns([3, 1])
with c_head1:
    # --- CAMBIO AQUÍ: Título en Español ---
    st.title("🏦 Gestor de Patrimonio con Inteligencia Artificial")
    st.caption("Planificación Financiera Automatizada • Algoritmo v2.4")

st.markdown("---")

# ==============================================================================
# 🎛️ PANEL DE CONTROL (DENTRO DE UNA "TARJETA")
# ==============================================================================
with st.container():
    st.markdown("<div style='background-color: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #eee;'>", unsafe_allow_html=True)
    
    st.subheader("⚙️ Configuración de Cartera")
    
    c1, c2, c3 = st.columns([2, 2, 1])
    
    with c1:
        capital = st.number_input("Capital Inicial (€)", min_value=1000.0, value=10000.0, step=500.0, format="%.2f")
    
    with c2:
        perfil = st.selectbox("Perfil de Inversor", ["🐢 Conservador (Bajo Riesgo)", "⚖️ Moderado (Equilibrado)", "🚀 Dinámico (Alto Rendimiento)"])
    
    with c3:
        st.write(" ")
        st.write(" ")
        boton_generar = st.button("🚀 GENERAR ESTRATEGIA")
        
    if "Dinámico" in perfil:
        st.caption("⚠️ **Aviso de Riesgo:** Este perfil prioriza el crecimiento sobre la seguridad. Volatilidad esperada: Alta.")
    else:
        st.caption("✅ **Perfil Seguro:** Priorizamos preservación de capital y empresas sólidas (Blue Chips).")

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# ==============================================================================
# 📊 RESULTADOS (SECCIÓN DASHBOARD)
# ==============================================================================
if boton_generar:
    
    with st.spinner("🔄 Conectando con mercados globales (NYSE, NASDAQ, BME)..."):
        try:
            df_todos = datos.descargar_datos(datos.EMPRESAS_SELECCIONADAS)
            factor_eur = datos.obtener_precio_dolar()
        except: st.error("Error de conexión API."); st.stop()

    # --- LÓGICA DE NEGOCIO ---
    todos = []
    if "Conservador" in perfil: p_seg, p_mod, p_risk = 0.8, 0.2, 0.0
    elif "Moderado" in perfil:    p_seg, p_mod, p_risk = 0.6, 0.4, 0.0
    else:                         p_seg, p_mod, p_risk = 0.2, 0.4, 0.4
    
    for t in datos.EMPRESAS_SELECCIONADAS:
        try:
            est, _, prec, vol = calculos.analizar_semaforo(df_todos, t)
            if est == "VERDE":
                nota, _ = analisis_fundamental.analizar_calidad_fundamental(t)
                precio_e = prec * factor_eur if not t.endswith(".MC") else prec
                todos.append({"T": t, "E": datos.NOMBRES.get(t, t), "P": precio_e, "N": nota, "V": vol})
        except: pass

    c_seg = [x for x in todos if x["N"] >= 7 and x["V"] <= 0.01]
    c_mod = [x for x in todos if x["N"] >= 7 and 0.01 < x["V"] <= 0.015]
    c_rsk = [x for x in todos if x["V"] > 0.015]

    cartera = []
    def asignar(lista, pct, etiqueta):
        if pct == 0: return
        dinero = capital * pct
        if not lista:
            if etiqueta == "Riesgo" and todos: lista = sorted(todos, key=lambda x: x["V"], reverse=True)[:3]
            elif etiqueta == "Equilibrio" and c_seg: lista = c_seg
            else: return
            
        seleccion = sorted(lista, key=lambda x: x["N"], reverse=True)[:3] if etiqueta != "Riesgo" else sorted(lista, key=lambda x: x["V"], reverse=True)[:3]
        if not seleccion: return
        
        dinero_acc = dinero / len(seleccion)
        for a in seleccion:
            n_acc = max(1, int(dinero_acc / a["P"]))
            tot = n_acc * a["P"]
            cartera.append({"Categoría": etiqueta, "Activo": a["E"], "Precio": a["P"], "Cantidad": n_acc, "Total": tot, "Calidad": a["N"]})

    asignar(c_seg, p_seg, "🛡️ Preservación")
    asignar(c_mod, p_mod, "⚖️ Crecimiento")
    asignar(c_rsk, p_risk, "🔥 Especulativo")

    # --- VISUALIZACIÓN ---
    if cartera:
        df_c = pd.DataFrame(cartera)
        total_real = df_c["Total"].sum()
        cash = capital - total_real
        
        # 1. TARJETAS DE MÉTRICAS
        st.markdown("### 📊 Resumen de la Propuesta")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Inversión Total", f"{total_real:,.2f} €")
        k2.metric("Liquidez (Cash)", f"{cash:,.2f} €")
        k3.metric("Activos", f"{len(df_c)}")
        k4.metric("Calidad Media", f"{df_c['Calidad'].mean():.1f}/10")
        
        st.markdown("---")
        
        # 2. SECCIÓN VISUAL
        g_col, t_col = st.columns([1, 2])
        
        with g_col:
            fig = px.pie(df_c, values='Total', names='Categoría', hole=0.6, color='Categoría',
                         color_discrete_map={"🛡️ Preservación":"#27AE60", "⚖️ Crecimiento":"#F39C12", "🔥 Especulativo":"#C0392B"})
            fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"<div style='text-align: center; color: gray;'>Diversificación por Estrategia</div>", unsafe_allow_html=True)

        with t_col:
            st.markdown("#### 🧾 Orden de Compra")
            
            df_display = df_c.copy()
            df_display["Precio"] = df_display["Precio"].apply(lambda x: f"{x:.2f} €")
            df_display["Total"] = df_display["Total"].apply(lambda x: f"{x:.2f} €")
            
            st.dataframe(
                df_display[["Categoría", "Activo", "Cantidad", "Precio", "Total"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Categoría": st.column_config.TextColumn("Estrategia"),
                    "Total": st.column_config.TextColumn("Importe Neto"),
                }
            )
            
            # BOTÓN DE DESCARGA CSV (FUNCIONA DE VERDAD)
            csv = df_c.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Descargar Orden en CSV (Excel)",
                data=csv,
                file_name="mi_cartera_optimizada.csv",
                mime="text/csv",
                type="secondary",
                use_container_width=True
            )

    else:
        st.warning("El algoritmo no ha encontrado oportunidades que cumplan sus criterios estrictos hoy.")

else:
    st.info("👋 Configure sus parámetros arriba y pulse 'Generar Estrategia' para comenzar.")

# --- AÑADIR AL FINAL DE CADA ARCHIVO .PY ---

# Barra lateral con información del desarrollador y donaciones
with st.sidebar:
    st.markdown("---")
    st.markdown("### 👨‍💻 Sobre el Proyecto")
    st.caption("Desarrollado con ❤️ usando Python y Streamlit.")
    
    st.markdown("") # Espacio
    
    # Botón de Donación Estilizado
    st.markdown("¿Te ha sido útil?")
    st.link_button(
        label="☕ Invítame a un café", 
        url="https://www.paypal.com/paypalme/TU_USUARIO", # <--- PON AQUÍ TU LINK REAL (PayPal o Ko-fi)
        type="primary", 
        use_container_width=True
    )
    
    st.caption("v2.5.0 - Stable Release")
