# src/features.py
import math
import re
from collections import Counter
import tldextract
import pandas as pd

class AdvancedFeatureExtractor:
    def __init__(self):
        self.suspicious_keywords = [
            'login', 'signin', 'logon', 'update', 'verify', 'secure', 'account', 
            'banking', 'confirm', 'password', 'free', 'bonus', 'ebay', 'paypal'
        ]
        self.shorteners = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs"

    def entropy(self, string):
        p, lns = Counter(string), float(len(string))
        return -sum(count/lns * math.log(count/lns, 2) for count in p.values())

    def digit_ratio(self, string):
        if len(string) == 0: return 0
        return sum(c.isdigit() for c in string) / len(string)

    def extract_features(self, df):
        # Si nos llega una URL suelta (string) desde la API, la convertimos en DataFrame
        if isinstance(df, str): 
            df = pd.DataFrame([df], columns=['URL'])
            
        # --- 1. Estructura Básica ---
        df['url_len'] = df['URL'].apply(lambda x: len(str(x)))
        df['tld_obj'] = df['URL'].apply(lambda x: tldextract.extract(x))
        df['domain'] = df['tld_obj'].apply(lambda x: x.domain)
        df['subdomain'] = df['tld_obj'].apply(lambda x: x.subdomain)
        
        # --- 2. Características de "Caos" ---
        df['domain_entropy'] = df['domain'].apply(self.entropy)
        df['url_entropy'] = df['URL'].apply(self.entropy)
        
        # --- 3. Ratios ---
        df['digit_ratio_url'] = df['URL'].apply(self.digit_ratio)
        df['digit_ratio_domain'] = df['domain'].apply(self.digit_ratio)
        
        # --- 4. Conteo de Caracteres ---
        feature_chars = ['@', '.', '-', '%', '?', '=', 'http', 'https', 'www']
        for char in feature_chars:
            df[f'count_{char}'] = df['URL'].apply(lambda x: str(x).count(char))
            
        # --- 5. Ingeniería Social ---
        df['sus_keywords_count'] = df['URL'].apply(
            lambda x: sum(1 for word in self.suspicious_keywords if word in str(x).lower())
        )
        
        # --- 6. Longitudes ---
        df['domain_len'] = df['domain'].apply(len)
        df['subdomain_len'] = df['subdomain'].apply(len)
        
        # Limpieza (Solo devolvemos las columnas numéricas que espera el modelo)
        cols_to_keep = [
            'url_len', 'domain_len', 'subdomain_len', 'domain_entropy', 'url_entropy',
            'digit_ratio_url', 'digit_ratio_domain', 
            'count_@', 'count_.', 'count_-', 'count_%', 'count_?', 'count_=', 
            'count_http', 'count_https', 'count_www', 'sus_keywords_count'
        ]
        
        # Rellenamos con 0 si alguna columna falta por seguridad
        for col in cols_to_keep:
            if col not in df.columns:
                df[col] = 0
                
        return df[cols_to_keep]