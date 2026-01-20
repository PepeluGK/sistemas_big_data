import pandas as pd
from datetime import datetime, timedelta
import re


# 1 Identidad del script
print("Iniciando limpieza de Jose Luis Saavedra...")


# 2 Carga del dataset
df = pd.read_csv("ventas_big_data_ut3.csv")
filas_iniciales = len(df)


# 3 Eliminación de duplicados
df_sin_duplicados = df.drop_duplicates()
filas_eliminadas_duplicados = filas_iniciales - len(df_sin_duplicados)
df = df_sin_duplicados.copy()


# 4 Normalización de productos
def normalizar_producto(valor):
    if pd.isna(valor):
        return valor
    valor = valor.strip()
    return valor.title()

df["producto"] = df["producto"].apply(normalizar_producto)


# 5 Tratamiento de precios
df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
mediana_precio = df["precio"].median()
df["precio"] = df["precio"].fillna(mediana_precio)


# 6 Validación de cantidades
registros_cantidades_negativas = df[df["cantidad"] < 0].shape[0]
df = df[df["cantidad"] >= 0]


# 7 Procesamiento de fechas
def procesar_fecha(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).lower().strip()
    hoy = datetime.now()

    if valor == "ayer":
        return (hoy - timedelta(days=1)).date().isoformat()

    match = re.match(r"hace\s+(\d+)\s+dias", valor)
    if match:
        dias = int(match.group(1))
        return (hoy - timedelta(days=dias)).date().isoformat()

    formatos = ["%d/%m/%Y", "%Y-%m-%d", "%m-%d-%Y"]
    for fmt in formatos:
        try:
            return datetime.strptime(valor, fmt).date().isoformat()
        except ValueError:
            continue

    try:
        return pd.to_datetime(valor, errors="coerce").date().isoformat()
    except Exception:
        return None


df["fecha"] = df["fecha"].apply(procesar_fecha)


# 8 Exportación a JSON
nombre_salida = "ventas_limpias_joseluis.json"
df.to_json(nombre_salida, orient="records", force_ascii=False, indent=4)


# 9 Bitacora de limpieza
print("\n--- Bitacora de Limpieza ---")
print(f"Total de filas iniciales: {filas_iniciales}")
print(f"Total de filas eliminadas por duplicidad: {filas_eliminadas_duplicados}")
print(f"Valor de la mediana utilizada para los precios: {round(mediana_precio, 2)}")
print(f"Número total de registros con cantidades negativas descartados: {registros_cantidades_negativas}")
print(f"Total de filas finales: {len(df)}")
