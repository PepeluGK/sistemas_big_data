import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

print("Iniciando Análisis ANBU - Detección de Anomalías")

# Cargar dataset
df = pd.read_csv("misiones_limpias.csv")

# ==============================
# 1 EL OJO DE LA VERDAD
# ==============================

print("\n--- Estadísticas Generales ---")
print(df["Nivel_Chakra"].describe())

media = df["Nivel_Chakra"].mean()
desviacion = df["Nivel_Chakra"].std()

print(f"\nMedia de chakra: {media}")
print(f"Desviación estándar: {desviacion}")
print(f"Valor máximo: {df['Nivel_Chakra'].max()}")

# ==============================
# 2 JUTSU DE VISUALIZACIÓN
# ==============================

plt.figure(figsize=(8,6))
sns.boxplot(y=df["Nivel_Chakra"], color="orange")
plt.title("Boxplot - Nivel de Chakra")
plt.show()

# ==============================
# 3 REGLA DE LOS 3 SIGMAS
# ==============================

df["Z_Score"] = (df["Nivel_Chakra"] - media) / desviacion

outliers = df[(df["Z_Score"] > 3) | (df["Z_Score"] < -3)]

print("\n--- OUTLIERS DETECTADOS (Z > 3 o Z < -3) ---")
print(outliers.head())

# ==============================
# 4 CAZA MAYOR
# ==============================

# Chakra negativo
chakra_negativo = df[df["Nivel_Chakra"] < 0]
print("\n--- Chakra Negativo ---")
print(chakra_negativo.head())

# Aldea desconocida
aldea_desconocida = df[df["Aldea"] == "Desconocida"]
print("\n--- Aldea Desconocida ---")
print(aldea_desconocida.head())

# Super Ninjas (2 < Z < 3)
super_ninjas = df[(df["Z_Score"] > 2) & (df["Z_Score"] < 3)]
print("\n--- Super Ninjas (2 < Z < 3) ---")
print(super_ninjas.head())

# ==============================
# 5 INTERROGATORIO FINAL
# ==============================

print("\n--- Datos completos de los sospechosos ---")
print(outliers)