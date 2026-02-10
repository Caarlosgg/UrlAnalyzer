# 🕵️‍♂️ URLAnalyzer: AI Phishing Detector (WIP)

![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![ML](https://img.shields.io/badge/Model-XGBoost-green)
![Framework](https://img.shields.io/badge/API-FastAPI-teal)

> **Nota:** Este proyecto está en fase temprana de desarrollo. La lógica de detección y el calibrado de probabilidades están siendo optimizados continuamente.

## 📖 Descripción

**URLAnalyzer** es un sistema inteligente diseñado para detectar URLs fraudulentas (Phishing) analizando patrones léxicos y matemáticos en tiempo real. A diferencia de las listas negras tradicionales, este sistema utiliza un modelo de Machine Learning (**XGBoost**) para predecir la maliciosidad de una URL basándose en su estructura (entropía, longitud, caracteres especiales, etc.).

## 🚀 Arquitectura del Proyecto

El sistema se divide en tres módulos principales:

1.  **Feature Extraction (`src/`)**: Motor matemático que descompone una URL en 17 características numéricas (Entropía de Shannon, Ratios de dígitos, Longitud de dominio, etc.).
2.  **API Rest (`api/`)**: Construida con **FastAPI**, sirve el modelo ML y gestiona las solicitudes de predicción. Incluye una *Whitelist* de alto rendimiento para sitios conocidos (YouTube, Twitch, Google).
3.  **Frontend (`frontend/`)**: Interfaz interactiva construida con **Streamlit** que muestra el nivel de riesgo, gráficos de confianza y telemetría técnica en tiempo real.

## 📂 Estructura de Carpetas

```text
PHISHING-DETECTION/
├── api/
│   └── main.py           # Servidor FastAPI (Inferencia y Endpoints)
├── data/
│   ├── raw/              # Datasets originales
│   └── processed/        # Datos limpios y procesados para el modelo
├── frontend/
│   └── main.py           # Interfaz de usuario (Streamlit Dashboard)
├── models/
│   └── modelo_xgboost... # Archivos .pkl (Modelo serializado + Metadatos)
├── src/
│   ├── features.py       # Extractor de características (Core Matemático)
│   ├── 3_entrenamiento.py # Script de entrenamiento y optimización ML
│   └── ...               # Scripts auxiliares de análisis
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación
```

## 🛠️ Instalación y Uso

### Prerrequisitos
* Python 3.10 o superior
* Git

### 1. Clonar el repositorio

```bash
git clone [https://github.com/TU_USUARIO/URLAnalyzer.git](https://github.com/TU_USUARIO/URLAnalyzer.git)
cd URLAnalyzer
```

### 2. Entorno Virtual e Instalación

```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Windows:
.venv\Scripts\activate
# Activar en Mac/Linux:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Ejecutar el Sistema (Doble Terminal)

Para que el sistema funcione, necesitas dos terminales abiertas simultáneamente:

**Terminal 1: La API (Backend)**

```bash
python -m uvicorn api.main:app --reload
```
*Esperar a ver el mensaje: "Application startup complete"*

**Terminal 2: El Frontend**

```bash
streamlit run frontend/main.py
```
*Esto abrirá automáticamente el navegador con la interfaz gráfica.*

## ⚙️ Estado Actual (Day 1)

Actualmente, el sistema es funcional pero experimental.

- [x] **Extracción de características:** Análisis léxico (longitud, símbolos, https, www).
- [x] **Matemáticas:** Cálculo de Entropía de Shannon para detectar aleatoriedad en dominios.
- [x] **Modelo:** Entrenamiento inicial con XGBoost y optimización de hiperparámetros.
- [x] **Backend:** API funcional con alineación dinámica de características (evita errores de dimensionalidad).
- [x] **Frontend:** Interfaz gráfica con medidor de riesgo (Gauge Chart) y telemetría.
- [ ] **En proceso:** Calibración fina de probabilidades (corregir sesgos estadísticos).
- [ ] **En proceso:** Detección avanzada de marcas en subdominios (Feature Engineering).

## 🔮 Próximos Pasos (Roadmap)

* Mejorar el dataset con técnicas de balanceo (SMOTE) para evitar overfitting.
* Implementar `CalibratedClassifierCV` para obtener probabilidades reales (0-100%).
* Dockerizar la aplicación para un despliegue sencillo en la nube.
* Añadir soporte para detección de ataques homógrafos (Punycode).

## ⚠️ Disclaimer

Este software es una prueba de concepto (PoC) educativa y de investigación. No debe utilizarse como única capa de seguridad en entornos de producción críticos sin una auditoría previa.


