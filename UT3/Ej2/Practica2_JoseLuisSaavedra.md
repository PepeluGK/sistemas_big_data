# Práctica 2: El Pergamino Infinito (Consumo de APIs)

En esta misión, usarás tus habilidades diplomáticas para extraer información de la PokéAPI. El objetivo es obtener una lista de elementos, sus estadísticas y transformarlas en información útil para la aldea.

## Pergamino Digital ANBU

### Objetivo
Crear un script en Python que consuma datos paginados de una API REST y los almacene en un archivo local.

### ¿Por qué hacemos esto?
En el análisis de Big Data, la extracción (el primer paso del proceso ETL) es fundamental. Extraemos estos datos con un propósito claro:

- **Análisis de Distribución:** ¿Están equilibrados los tipos? Sin los datos en bruto, no podemos hacer estadísticas.
- **Preparación para Machine Learning:** En unidades posteriores, utilizaremos este “pergamino” para entrenar modelos predictivos.
- **Independencia de Datos:** Al guardar los datos localmente, evitamos saturar la API con peticiones repetitivas.

### Estructura de los datos del Pergamino
Al invocar la PokéAPI para obtener listas, recibirás un objeto JSON con esta estructura. Identificar estas claves es el primer paso para dominar la paginación:

- `count`: Total de registros en el palacio digital.  
- `next`: URL de la siguiente página (tu guía para el bucle while).  
- `previous`: URL de la anterior.  
- `results`: La lista de ninjas (Pokémon) detectados, con su nombre y URL de detalles.

## Requisitos
- Librería `requests` y `pandas` instaladas (`pip install requests pandas`).  
- Conexión a Internet para contactar con la API.

## Ejercicio paso a paso

### Importaciones
```python
    import requests
    import pandas as pd
    import time
```

### URL
```python
    url = "https://pokeapi.co/api/v2/pokemon?limit=20"
    todos_los_pokemon = []
```

### Paginación
```python
    while url:
        print(f"Consultando: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        todos_los_pokemon.extend(data["results"])
        
        url = data["next"]
        
        time.sleep(0.5)

    print(f"Total de Pokémon recolectados: {len(todos_los_pokemon)}")
```

### Datos pokemon
```python
    pokemon_detalles = []

    for pokemon in todos_los_pokemon:
        detalle_url = pokemon["url"]
        
        response = requests.get(detalle_url)
        response.raise_for_status()
        detalle = response.json()
        
        pokemon_detalles.append({
            "name": detalle["name"],
            "height": detalle["height"],
            "weight": detalle["weight"],
            "base_experience": detalle["base_experience"]
        })
        
        time.sleep(0.3)
```

### DataFrame
```python
    df = pd.DataFrame(pokemon_detalles)
```

### Conversion e IMC
```python
    df["height_m"] = df["height"] / 10
    df["weight_kg"] = df["weight"] / 10
    df["imc"] = df["weight_kg"] / (df["height_m"] ** 2)
```

### Guardar Pergamino
```python
    df.to_csv("pokemon_final.csv", index=False)
    df.to_json("pokemon_final.json", orient="records", indent=4)

    print("✅ Archivos guardados:")
    print(" - pokemon_final.csv")
    print(" - pokemon_final.json")
```

## Preguntas de reflexión
1. ¿Por qué es importante actualizar la URL con el enlace `next` en lugar de simplemente incrementar un número de página manualmente?  

Porque la API decide cómo se pagina. Usar next garantiza que sigues el orden correcto y evita errores si la API cambia su lógica.

2. ¿Qué ventaja tiene normalizar las unidades (como pasar de decímetros a metros) dentro del propio proceso ETL en lugar de hacerlo después en una hoja de cálculo?  

Deja los datos listos y consistentes desde el origen, reduce errores manuales y facilita reutilizar los datos después.

3. Si la API tuviera un límite de 1000 registros por página, ¿cómo afectaría esto al rendimiento de tu script?

Habría menos peticiones HTTP, lo que podría acelerar el proceso. Pero cada página sería más grande, usando más memoria; si la página fuera demasiado grande, el script podría volverse lento o incluso fallar en PC con poca RAM.