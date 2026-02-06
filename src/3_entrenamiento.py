import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, precision_recall_curve

# Configuración
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "dataset_features.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo_xgboost_optimizado.pkl")
METRICS_PATH = os.path.join(BASE_DIR, "data", "processed", "confusion_matrix_opt.png")

def buscar_mejor_modelo():
    print("⚡ Cargando datos para optimización...")
    if not os.path.exists(DATA_PATH):
        return
        
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=['target'])
    y = df['target']
    
    # División
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Calcular scale_pos_weight inicial
    ratio = float(np.sum(y_train == 0)) / np.sum(y_train == 1)
    print(f"⚖️  Ratio de desbalance base: {ratio:.2f}")

    # --- 1. DEFINIR LA REJILLA DE BÚSQUEDA (GRID) ---
    # Le damos opciones al modelo para que pruebe
    param_grid = {
        'n_estimators': [200, 400, 600, 800],        # Cantidad de árboles
        'learning_rate': [0.01, 0.05, 0.1, 0.2],     # Velocidad de aprendizaje
        'max_depth': [6, 8, 10, 12],                 # Profundidad (complejidad)
        'subsample': [0.7, 0.8, 0.9],                # Evitar overfitting
        'colsample_bytree': [0.7, 0.8, 0.9],
        'scale_pos_weight': [ratio, ratio * 1.2, ratio * 0.8], # Probar variaciones del peso
        'gamma': [0, 0.1, 0.2]                       # Regularización
    }

    xgb = XGBClassifier(random_state=42, n_jobs=-1, objective='binary:logistic')

    # --- 2. BÚSQUEDA ALEATORIA (Randomized Search) ---
    print("\n🔍 Iniciando búsqueda de hiperparámetros (Esto puede tardar unos minutos)...")
    print("   Estamos probando 20 combinaciones con validación cruzada de 3 pliegues.")
    
    search = RandomizedSearchCV(
        estimator=xgb,
        param_distributions=param_grid,
        n_iter=20,              # Probará 20 combinaciones aleatorias
        scoring='f1',           # Optimizar para F1-Score (equilibrio precision/recall)
        cv=3,                   # 3 validaciones por combinación
        verbose=1,
        random_state=42,
        n_jobs=-1
    )
    
    search.fit(X_train, y_train)
    
    best_model = search.best_estimator_
    print(f"\n✅ ¡Mejores parámetros encontrados!: {search.best_params_}")

    # --- 3. BÚSQUEDA DE UMBRAL ÓPTIMO (Threshold Tuning) ---
    print("\n🎯 Buscando el umbral de decisión perfecto...")
    y_prob = best_model.predict_proba(X_test)[:, 1]
    
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_prob)
    
    # Buscamos el umbral que nos da el mejor F1 Score
    fscore = (2 * precisions * recalls) / (precisions + recalls)
    ix = np.argmax(fscore)
    best_thresh = thresholds[ix]
    
    print(f"   Umbral Óptimo: {best_thresh:.4f}")
    print(f"   F1-Score esperado: {fscore[ix]:.4f}")

    # --- 4. EVALUACIÓN FINAL CON UMBRAL AJUSTADO ---
    # Aplicamos el umbral personalizado
    y_pred_opt = (y_prob >= best_thresh).astype(int)

    print("\n" + "="*40)
    print("🏆 RESULTADOS FINALES OPTIMIZADOS")
    print("="*40)
    print(f"Accuracy: {accuracy_score(y_test, y_pred_opt):.4f}")
    print(f"ROC-AUC:  {roc_auc_score(y_test, y_prob):.4f}")
    
    print("\n📋 REPORTE DETALLADO:")
    print(classification_report(y_test, y_pred_opt, target_names=['Legítimo', 'Phishing']))

    # Guardar matriz
    plt.figure(figsize=(10, 8))
    cm = confusion_matrix(y_test, y_pred_opt)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
                xticklabels=['Pred: Seguro', 'Pred: Phishing'],
                yticklabels=['Real: Seguro', 'Real: Phishing'])
    plt.title(f'Matriz Optimizada (Umbral: {best_thresh:.2f})')
    plt.savefig(METRICS_PATH)
    
    # Guardamos el modelo y el umbral (en un diccionario para no perder el dato)
    final_pack = {
        'model': best_model,
        'threshold': best_thresh
    }
    joblib.dump(final_pack, MODEL_PATH)
    print(f"\n💾 Modelo + Umbral guardados en: {MODEL_PATH}")

if __name__ == "__main__":
    buscar_mejor_modelo()