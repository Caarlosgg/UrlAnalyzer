import pandas as pd
import numpy as np
import re
import math
import tldextract
import os
from collections import Counter

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "dataset_phishing.csv")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "dataset_features.csv")

class AdvancedFeatureExtractor:
    def __init__(self):
        # Palabras que usan los hackers para dar confianza
        self.suspicious_keywords = [
            'login', 'signin', 'logon', 'update', 'verify', 'secure', 'account', 
            'banking', 'confirm', 'password', 'free', 'bonus', 'ebay', 'paypal'
        ]
        self.shorteners = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs"

    def entropy(self, string):
        """Calcula la 'aleatoriedad' de un texto. 
        Un texto normal tiene entropía baja. 'akj38f83' tiene entropía alta."""
        p, lns = Counter(string), float(len(string))
        return -sum(count/lns * math.log(count/lns, 2) for count in p.values())

    def digit_ratio(self, string):
        """Porcentaje de números en el string"""
        if len(string) == 0: return 0
        return sum(c.isdigit() for c in string) / len(string)

    def extract_features(self, df):
        print("🚀 Iniciando extracción AVANZADA de características...")
        
        # --- 1. Estructura Básica ---
        df['url_len'] = df['URL'].apply(lambda x: len(str(x)))
        df['tld_obj'] = df['URL'].apply(lambda x: tldextract.extract(x))
        df['domain'] = df['tld_obj'].apply(lambda x: x.domain)
        df['subdomain'] = df['tld_obj'].apply(lambda x: x.subdomain)
        
        # --- 2. Características de "Caos" (Entropía) ---
        print("   -> Calculando Entropía y Complejidad...")
        # La entropía del dominio detecta nombres generados por máquinas (DGA)
        df['domain_entropy'] = df['domain'].apply(self.entropy)
        df['url_entropy'] = df['URL'].apply(self.entropy)
        
        # --- 3. Ratios Sospechosos ---
        # Los sitios legítimos suelen tener pocas cifras (google.com vs google12355.com)
        df['digit_ratio_url'] = df['URL'].apply(self.digit_ratio)
        df['digit_ratio_domain'] = df['domain'].apply(self.digit_ratio)
        
        # --- 4. Conteo de Caracteres Específicos ---
        print("   -> Buscando anomalías en caracteres...")
        feature_chars = ['@', '.', '-', '%', '?', '=', 'http', 'https', 'www']
        for char in feature_chars:
            df[f'count_{char}'] = df['URL'].apply(lambda x: str(x).count(char))
            
        # --- 5. Ingeniería Social (Palabras clave) ---
        print("   -> Detectando palabras trampa...")
        df['sus_keywords_count'] = df['URL'].apply(
            lambda x: sum(1 for word in self.suspicious_keywords if word in str(x).lower())
        )
        
        # --- 6. Longitudes específicas ---
        df['domain_len'] = df['domain'].apply(len)
        df['subdomain_len'] = df['subdomain'].apply(len)
        
        # --- 7. Target Mapping ---
        df['target'] = df['Label'].map({'good': 0, 'bad': 1})
        
        # Limpieza final
        cols_to_drop = ['URL', 'Label', 'tld_obj', 'domain', 'subdomain']
        df_final = df.drop(columns=cols_to_drop)
        
        return df_final

def main():
    print(f"📥 Cargando datos desde {RAW_PATH}")
    df = pd.read_csv(RAW_PATH)
    
    # Eliminamos duplicados primero para ahorrar tiempo de cómputo
    df = df.drop_duplicates()
    
    extractor = AdvancedFeatureExtractor()
    df_processed = extractor.extract_features(df)
    
    print(f"💾 Guardando dataset PRO (Dimensiones: {df_processed.shape})")
    df_processed.to_csv(PROCESSED_PATH, index=False)
    print("✅ ¡Procesamiento Avanzado Completado!")

if __name__ == "__main__":
    main()