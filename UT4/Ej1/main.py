import pandas as pd

# 1. Carga del pergamino secreto
df = pd.read_csv('registros_misiones.csv')

# --- SECCIÓN 1: LIMPIEZA DE DATOS ---

def limpiar_registro(df):

    # Reto 1: eliminar duplicados
    duplicados = df.duplicated().sum()
    print(f"Registros duplicados encontrados: {duplicados}")
    df = df.drop_duplicates()

    # Reto 2: estandarizar 'aldea'
    df['aldea'] = df['aldea'].str.strip().str.title()

    # Reto 3: rellenar ninjas anónimos de Kiri
    df.loc[
        (df['nin_id'].isna()) & (df['aldea'] == 'Kiri'),
        'nin_id'
    ] = 'Ninja de la Niebla Anonimo'

    # Reto 4: convertir fecha
    df['ts'] = pd.to_datetime(df['ts'], errors='coerce')

    # Reto 5: limpiar chakra imposible
    df = df[(df['chakra'] > 0) & (df['chakra'] <= 100000)]

    # Reto 6: renombrar columnas
    df = df.rename(columns={
        'id_reg': 'ID',
        'ts': 'Fecha',
        'nin_id': 'Ninja',
        'status': 'Estado',
        'desc': 'Descripcion'
    })

    return df


# --- SECCIÓN 2: BÚSQUEDA Y CONSULTAS ---

def realizar_consultas(df):

    # Reto 7: palabras clave
    amenazas = df[df['Descripcion'].str.contains(
        'espía|sospechoso|enemigo',
        case=False,
        na=False
    )]
    print("\n--- Amenazas Detectadas ---")
    print(amenazas.head())

    # Reto 8: ninjas de Amegakure con chakra > 5000 y rango != D
    infiltrados = df[
        (df['aldea'] == 'Amegakure') &
        (df['chakra'] > 5000) &
        (df['rango'] != 'D')
    ]
    print("\n--- Infiltrados de la Lluvia ---")
    print(infiltrados.head())

    # Reto 9: accesos de madrugada (23:00 - 05:00)
    madrugada = df[
        (df['Fecha'].dt.hour >= 23) |
        (df['Fecha'].dt.hour <= 5)
    ]
    print("\n--- Movimientos en la Madrugada ---")
    print(madrugada.head())

    # Reto 10: Top 5 chakra por aldea
    top5 = df.sort_values('chakra', ascending=False) \
             .groupby('aldea') \
             .head(5)
    print("\n--- Top 5 Ninjas por Aldea ---")
    print(top5[['aldea', 'Ninja', 'chakra']])

    # Reto 11: ninjas fuera de la alianza
    alianza = ['Konoha', 'Suna', 'Kumo']
    extranjeros = df[~df['aldea'].isin(alianza)]
    print("\n--- Ninjas fuera de la Alianza ---")
    print(extranjeros.head())

    # Reto 12: misiones fallidas por aldea
    fallos = df[df['Estado'] == 'Fallo'] \
                .groupby('aldea') \
                .size()
    print("\n--- Misiones Fallidas por Aldea ---")
    print(fallos)


# --- EJECUCIÓN DEL PROTOCOLO ANBU ---

print("Iniciando Rastreo de Chakra de Jose Luis Saavedra...")

df_limpio = limpiar_registro(df)
realizar_consultas(df_limpio)

df_limpio.to_csv('misiones_limpias_JoseLuis.csv', index=False)