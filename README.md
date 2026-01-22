# 🚀 El Chivato Bursátil: Edición IA

**El Chivato Bursátil** es una plataforma interactiva de análisis financiero diseñada para democratizar la inversión inteligente. Este proyecto evoluciona el análisis tradicional combinando datos de mercado en tiempo real con la potencia de la **Inteligencia Artificial Generativa (Google Gemini)** para ofrecer informes cualitativos instantáneos.

## 🌟 Funcionalidades Principales

### 🧠 1. Analista Inteligente (Nuevo)
* **Motor Híbrido:** Fusiona datos cuantitativos exactos (precios, PER, capitalización descargados de Yahoo Finance) con el razonamiento cualitativo de la IA.
* **Buscador Universal "Detective":** Gracias a la IA, puedes buscar empresas por su nombre común (ej. "Zara", "Google", "Ferrari") y el sistema localiza automáticamente su código bursátil (Ticker) en cualquier mercado del mundo.
* **Informes Automáticos:** Genera explicaciones textuales sobre si una acción está cara o barata, el sentimiento de las noticias recientes y una conclusión de inversión (Comprar/Vender/Esperar).

### 🔍 2. Analizador Técnico y Fundamental (Clásico)
* **Semáforo de Mercado:** Escáner en tiempo real con doble capa de análisis: Filtro Técnico (Tendencia) + Auditoría Fundamental (Notas 0-10 basadas en ratios).
* **Datos en Tiempo Real:** Conexión directa con mercados de España, EE.UU. y Europa.

### 🤖 3. Robo-Advisor (Gestión de Carteras)
* **Asset Allocation:** Algoritmo de asignación de activos.
* **Perfiles de Riesgo:** Generación de carteras personalizadas (Conservador, Moderado, Arriesgado) basadas en volatilidad y calidad.

### 📈 4. Visualización Avanzada
* **Gráficos Interactivos:** Visualización de la evolución del precio (último año) con gráficos de línea interactivos nativos de Streamlit.
* **Indicadores Visuales:** Métricas clave (Precio, PER, Variación %) con colores semánticos (Verde/Rojo) para una lectura rápida.

---

## 📂 Estructura del Proyecto

El código sigue una arquitectura modular y segura:

* **`web.py`**: 🧠 **Nuevo Núcleo IA.** Interfaz principal que conecta Streamlit, Yahoo Finance y Google Gemini.
* `Portada.py`: Landing Page original del proyecto.
* `requirements.txt`: Lista de dependencias necesarias para la nube.
* `calculos.py` / `analisis_fundamental.py`: Motores matemáticos para el análisis clásico.
* `pages/`: Módulos del Semáforo y el Robo-Advisor.

---

## 🛠️ Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/El_Chivato_Bursatil.git](https://github.com/TU_USUARIO/El_Chivato_Bursatil.git)
cd El_Chivato_Bursatil

