# 🚀 El Chivato Bursátil

![Estado](https://img.shields.io/badge/Estado-Terminado-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red)

**El Chivato Bursátil** es una plataforma interactiva de análisis financiero diseñada para democratizar la inversión inteligente. Combina análisis técnico, fundamental y algoritmos de gestión de riesgo para ayudar a estudiantes e inversores a tomar decisiones informadas.

## 🌟 Funcionalidades Principales

1.  **🔍 Analizador (Semáforo):**
    * Escáner de mercado en tiempo real (España y EE.UU.).
    * **Doble Capa de Análisis:** Filtro Técnico (Tendencia) + Auditoría Fundamental (Notas 0-10 basadas en ratios financieros).
    * Buscador específico con generación de informes automáticos y conversión de divisa a Euros.

2.  **🤖 Robo-Advisor (Inversor):**
    * Algoritmo de asignación de activos (*Asset Allocation*).
    * Generación de carteras personalizadas según perfil de riesgo (Conservador, Moderado, Arriesgado).
    * Diversificación automática basada en volatilidad y calidad.

3.  **📈 Visualización Avanzada:**
    * Gráficos interactivos (Plotly) y estáticos (Matplotlib).
    * Indicadores visuales semánticos (Semáforos, Tablas de colores).

## 📂 Estructura del Proyecto

El código sigue una arquitectura modular para facilitar el mantenimiento:

* `Portada.py`: 🏠 Punto de entrada de la aplicación (Landing Page).
* `datos.py`: 📡 Módulo de conexión con la API de Yahoo Finance (Descarga segura).
* `calculos.py`: 🧮 Motor matemático para análisis técnico y volatilidad.
* `analisis_fundamental.py`: 🔬 Auditor contable (PER, Deuda, Márgenes...).
* `graficos.py`: 🎨 Generador de gráficos lineales.
* `pages/`:
    * `Analizador.py`: Lógica del Semáforo y Buscador.
    * `Inversor.py`: Lógica del Robo-Advisor.

## 🛠️ Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/El_Chivato_Bursatil.git](https://github.com/TU_USUARIO/El_Chivato_Bursatil.git)
    cd El_Chivato_Bursatil
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación:**
    Es importante ejecutar el archivo `Portada.py`:
    ```bash
    streamlit run Portada.py
    ```

## 🤖 Transparencia y Autoría

Este proyecto ha sido desarrollado por **Julen Corral** como Proyecto Final de Python.

**Nota sobre el uso de Inteligencia Artificial:**
Este software ha sido creado utilizando **Inteligencia Artificial Generativa (LLMs)** como herramienta de apoyo al desarrollo (*AI-Assisted Development*). La IA ha actuado como "Copiloto" o tutor virtual para:
* Refactorización y limpieza de código.
* Depuración de errores (*Debugging*).
* Explicación de conceptos financieros y librerías complejas.
* Optimización de la estructura modular.

La lógica de negocio, la selección de estrategias de inversión y la arquitectura final han sido supervisadas y validadas por mí.

---

*Datos financieros proporcionados por Yahoo Finance. Proyecto con fines educativos, no constituye asesoramiento financiero real.*
