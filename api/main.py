from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import sys

# Añadimos src al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.features import AdvancedFeatureExtractor

app = FastAPI(
    title="Phishing Detection API (PRO)",
    description="API optimizada con XGBoost y Umbral Dinámico",
    version="2.0"
)

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo_xgboost_optimizado.pkl")

# Variables globales
model = None
threshold = 0.5 # Valor por defecto por si falla la carga
extractor = AdvancedFeatureExtractor()

# Carga al inicio
try:
    print(f"⚡ Cargando sistema inteligente desde: {MODEL_PATH}")
    artifact = joblib.load(MODEL_PATH)
    
    # DETALLE CLAVE: Ahora el .pkl es un diccionario, no el modelo directo
    model = artifact['model']
    threshold = artifact['threshold']
    
    print(f"✅ Sistema cargado. Umbral de corte optimizado: {threshold:.4f}")
except Exception as e:
    print(f"❌ ERROR CRÍTICO: No se pudo cargar el modelo. {e}")

class URLRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {
        "status": "online",
        "model_version": "XGBoost Optimized",
        "current_threshold": float(threshold)
    }

@app.post("/predict")
def predict(request: URLRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Modelo no cargado")
    
    # 1. Extracción de características
    try:
        features_df = extractor.extract_features(request.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando URL: {e}")

    # 2. Predicción de Probabilidad
    # Obtenemos la probabilidad de ser CLASE 1 (Phishing)
    prob_phishing = model.predict_proba(features_df)[0][1]
    
    # 3. Decisión usando el UMBRAL OPTIMIZADO (No el 0.5 estándar)
    es_phishing = prob_phishing >= threshold
    
    return {
        "url": request.url,
        "prediction": "PHISHING 🔴" if es_phishing else "LEGÍTIMO 🟢",
        "confidence": float(prob_phishing),
        "threshold_used": float(threshold),
        "risk_level": "CRÍTICO" if prob_phishing > 0.85 else ("ALTO" if es_phishing else "BAJO")
    }