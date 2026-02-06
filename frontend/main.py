import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="URLAnalyzer AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS (ESTILO HACKER/CYBER MEJORADO) ---
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    /* Títulos en estilo consola/hacker */
    h1, h2, h3 {
        color: #00FF99 !important;
        font-family: 'Courier New', monospace;
    }
    /* Estilo específico para el título del gráfico */
    .chart-title {
        color: #00FF99;
        font-family: 'Courier New', monospace;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00C853, #64DD17);
        color: black;
        border: none;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        transition: 0.3s;
        box-shadow: 0 0 10px rgba(0, 255, 153, 0.2);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px #00FF99;
        color: white;
    }
    .risk-critical {
        color: #FF4B4B;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 1.8rem;
        text-shadow: 0 0 10px rgba(255, 75, 75, 0.5);
    }
    .risk-safe {
        color: #00C853;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 1.8rem;
        text-shadow: 0 0 10px rgba(0, 200, 83, 0.5);
    }
    /* Input personalizado */
    .stTextInput>div>div>input {
        color: #00FF99;
        background-color: #161B22; 
        border: 1px solid #00FF99;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAR HISTORIAL EN MEMORIA ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- BARRA LATERAL (SIDEBAR PRO) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.title("URLAnalyzer v1.0")
    st.markdown("---")
    
    # Métricas rápidas
    c1, c2 = st.columns(2)
    c1.metric("Estado", "🟢 ON")
    c2.metric("Modelo", "XGBoost")
    
    st.markdown("---")
    st.caption("Herramienta de análisis forense digital.")
    
    # Sección de Autor
    st.markdown("### 👨‍💻 Developed by")
    st.markdown("**Carlos Gallardo González**")
    st.markdown("[GitHub](https://github.com/Caarlosgg) | [LinkedIn](https://linkedin.com)") 
    
    st.markdown("---")
    with st.expander("🛠️ Stack Técnico"):
        st.code("Python 3.10\nFastAPI\nXGBoost\nStreamlit\nPlotly", language="text")

# --- CABECERA ---
st.title("🕵️‍♂️ URLAnalyzer: Detector de Phishing")
st.markdown("#### Inteligencia Artificial entrenada para detectar fraudes digitales en tiempo real.")

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs(["🚀 Escáner en Vivo", "📜 Historial de Sesión", "ℹ️ Cómo Funciona"])

# === PESTAÑA 1: EL ESCÁNER ===
with tab1:
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        url_input = st.text_input("Pegue la URL sospechosa aquí:", placeholder="http://ejemplo-banco-falso.com", label_visibility="collapsed")
        st.caption("ℹ️ **Info:** El sistema calculará la entropía, longitud y reputación del dominio en milisegundos.")
    
    with col_btn:
        analyze_btn = st.button("ESCANEAR AHORA 🔍", use_container_width=True)

    if analyze_btn:
        if not url_input:
            st.warning("⚠️ Por favor ingresa una URL primero.")
        else:
            with st.spinner('🔄 La IA está analizando patrones matemáticos y léxicos...'):
                try:
                    # Llamada a TU API
                    response = requests.post(
                        "http://127.0.0.1:8000/predict",
                        json={"url": url_input}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        confidence = data['confidence']
                        is_phishing = data['prediction'] == "PHISHING 🔴"
                        
                        # Guardar en historial
                        st.session_state.history.insert(0, {
                            "Hora": datetime.now().strftime("%H:%M:%S"),
                            "URL": url_input,
                            "Resultado": data['prediction'],
                            "Confianza": f"{confidence*100:.2f}%"
                        })
                        
                        st.divider()
                        
                        # DISEÑO DE RESULTADOS (3 COLUMNAS)
                        c1, c2, c3 = st.columns([1.2, 2, 1])
                        
                        with c1:
                            st.subheader("DIAGNÓSTICO")
                            st.write("") # Espacio
                            if is_phishing:
                                st.markdown(f"<p class='risk-critical'>⛔ AMENAZA DETECTADA</p>", unsafe_allow_html=True)
                                st.error(f"Nivel de Riesgo: **{data['risk_level']}**")
                            else:
                                st.markdown(f"<p class='risk-safe'>✅ SITIO SEGURO</p>", unsafe_allow_html=True)
                                st.success(f"Nivel de Riesgo: **{data['risk_level']}**")
                            
                            st.metric("Confianza del Modelo", f"{confidence*100:.1f}%")

                        with c2:
                            # Título EXTERNO al gráfico para evitar superposición
                            st.markdown("<p class='chart-title'>PROBABILIDAD DE FRAUDE</p>", unsafe_allow_html=True)
                            
                            # Gráfico de Velocímetro (Gauge)
                            fig = go.Figure(go.Indicator(
                                mode = "gauge+number",
                                value = confidence * 100,
                                # Quitamos el título de aquí para que no se solape
                                gauge = {
                                    'axis': {'range': [None, 100], 'tickcolor': "white"},
                                    'bar': {'color': "#FF4B4B" if is_phishing else "#00C853"},
                                    'bgcolor': "#161B22",
                                    'borderwidth': 2,
                                    'bordercolor': "white",
                                    'steps': [
                                        {'range': [0, 50], 'color': "#1b5e20"},
                                        {'range': [50, 80], 'color': "#f57f17"},
                                        {'range': [80, 100], 'color': "#b71c1c"}
                                    ],
                                }
                            ))
                            # Ajustamos márgenes para que quede perfecto
                            fig.update_layout(
                                height=250, 
                                margin=dict(l=20,r=20,t=10,b=20), # t=10 porque el título está fuera
                                paper_bgcolor="rgba(0,0,0,0)",
                                font={'color': "white", 'family': "Courier New"}
                            )
                            st.plotly_chart(fig, use_container_width=True)

                        with c3:
                            st.subheader("TELEMETRÍA")
                            st.code(f"""
LEN: {len(url_input)}
SSL: {"TRUE" if "https" in url_input else "FALSE"}
THR: {data['threshold_used']:.2f}
IP : {data.get('is_ip', 'FALSE')}
                            """, language="yaml")

                    else:
                        st.error("Error 500: El cerebro de la IA no responde.")
                except Exception as e:
                    st.error(f"❌ Error de conexión: {e}. ¿Está corriendo la API en la otra terminal?")

# === PESTAÑA 2: HISTORIAL ===
with tab2:
    st.subheader("🕒 URLs analizadas recientemente")
    if st.session_state.history:
        df_history = pd.DataFrame(st.session_state.history)
        st.dataframe(df_history, use_container_width=True)
        
        if st.button("Borrar Historial"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("Aún no has analizado ninguna URL en esta sesión.")

# === PESTAÑA 3: CÓMO FUNCIONA (AMPLIADO) ===
with tab3:
    st.header("🧠 El Cerebro Digital: ¿Cómo funciona URLAnalyzer?")
    
    col_text, col_img = st.columns([2, 1])
    
    with col_text:
        st.markdown("""
        **URLAnalyzer** no es un simple antivirus que compara listas. Es un sistema de **Inteligencia Artificial** que "lee" la URL como lo haría un experto en ciberseguridad, pero millones de veces más rápido.
        
        ### 1. El Motor: XGBoost 🚀
        Utilizamos un algoritmo llamado **Extreme Gradient Boosting**. Imagina que tienes un consejo de **800 expertos** (árboles de decisión).
        * Cada experto mira la URL y vota si es segura o no basándose en reglas distintas.
        * El sistema combina todos los votos para dar un veredicto final con alta precisión.
        * **Optimizamos los pesos:** El modelo ha sido castigado duramente en el entrenamiento para priorizar no dejar pasar ni un solo virus (Recall alto).

        ### 2. Lo que la IA "ve" (Ingeniería de Características) 👁️
        La IA no lee texto, lee matemáticas. Convertimos la URL en números analizando:
        * **Entropía de Shannon:** ¿El dominio parece `google.com` (ordenado) o `x7f-3b.net` (caótico)?
        * **Patrones Léxicos:** Contamos puntos, guiones, arrobas y longitudes sospechosas.
        * **Ingeniería Social:** Buscamos palabras trampa como *'secure', 'login', 'update'* usadas para engañarte.
        
        ### 3. Rendimiento 📊
        * **Base de datos:** Entrenado con +500,000 URLs reales.
        * **Precisión Actual:** ~91%
        * **Umbral de Decisión:** Dinámico (0.59). No nos conformamos con el 50%, exigimos más certeza para marcar algo como amenaza.
        """)
    
    with col_img:
        st.info("💡 **Dato Curioso:**\n\nLa mayoría de los ataques de phishing hoy en día usan certificados HTTPS (el candadito verde). Por eso, URLAnalyzer **no confía** solo en el candado, sino que analiza la estructura profunda del enlace.")
        
        st.markdown("---")
        st.markdown("**Diagrama de Flujo:**")
        st.code("""
[USUARIO]
    ⬇️
[URLAnalyzer]
    ⬇️
[Extracción de Rasgos]
(Matemáticas + Texto)
    ⬇️
[IA XGBoost]
    ⬇️
[VEREDICTO]
        """, language="text")