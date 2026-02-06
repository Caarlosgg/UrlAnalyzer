import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de estilo 'Pro'
plt.style.use('ggplot')
sns.set_palette("husl")

def cargar_y_analizar():
    # 1. Ruta dinámica (funciona en cualquier PC)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "raw", "dataset_phishing.csv")

    print(f"🔄 Cargando datos desde: {file_path}...")

    if not os.path.exists(file_path):
        print("❌ ERROR: No encuentro el archivo 'dataset_phishing.csv' en data/raw/")
        return

    # Cargar CSV
    try:
        df = pd.read_csv(file_path)
        print("✅ ¡Datos cargados exitosamente!")
    except Exception as e:
        print(f"❌ Error al leer el CSV: {e}")
        return

    # 2. Información General
    print("\n" + "="*40)
    print("📊 RESUMEN DEL DATASET")
    print("="*40)
    print(f"Total de filas:    {df.shape[0]:,}")
    print(f"Total de columnas: {df.shape[1]}")
    print("-" * 30)
    print(df.info())

    # 3. Detección de Duplicados (CRÍTICO en Phishing)
    # Muchas veces el mismo ataque se reporta mil veces. Debemos saberlo.
    duplicados = df.duplicated().sum()
    porcentaje_dup = (duplicados / len(df)) * 100
    
    print("\n" + "="*40)
    print("⚠️ ANÁLISIS DE CALIDAD")
    print("="*40)
    print(f"Filas duplicadas: {duplicados:,} ({porcentaje_dup:.2f}%)")
    
    if porcentaje_dup > 10:
        print("👉 RECOMENDACIÓN: El dataset tiene muchos duplicados. Deberemos limpiarlos.")
    
    # 4. Balance de Clases
    # Asumimos que la columna etiqueta es la última o se llama 'Label'
    # Ajusta 'Label' si tu CSV tiene otro nombre (ej: 'status', 'class')
    target_col = 'Label' 
    
    if target_col in df.columns:
        conteo = df[target_col].value_counts()
        print("\n" + "="*40)
        print("⚖️ BALANCE DE CLASES")
        print("="*40)
        print(conteo)
        
        # Generar gráfico y guardarlo (No solo mostrarlo)
        plt.figure(figsize=(8, 5))
        sns.countplot(x=target_col, data=df)
        plt.title('Distribución: Phishing vs Legítimo')
        output_img = os.path.join(base_dir, "data", "processed", "distribucion_clases.png")
        plt.savefig(output_img)
        print(f"\n📸 Gráfico guardado en: {output_img}")
    else:
        print(f"\n⚠️ No encontré la columna '{target_col}'. Las columnas son: {df.columns.tolist()}")

if __name__ == "__main__":
    cargar_y_analizar()