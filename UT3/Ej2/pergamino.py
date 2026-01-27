import requests
import pandas as pd
import time

# 1. URL PokéAPI
url = "https://pokeapi.co/api/v2/pokemon?limit=20"
todos_los_pokemon = []

# 2. Bucle paginación
while url:
    print(f"Consultando: {url}")
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    todos_los_pokemon.extend(data["results"])
    
    url = data["next"]
    
    #time.sleep(0.5) lo quedo comentado por si se petase el programa y necesitase un descanso entre peticiones

print(f"Total de Pokémon recolectados: {len(todos_los_pokemon)}")

# 3. Datos de los Pokémon
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
    
    #time.sleep(0.3) lo quedo comentado por si se petase el programa y necesitase un descanso entre peticiones

# 4. Crear DataFrame
df = pd.DataFrame(pokemon_detalles)

# 5. Conversión de unidades + IMC
df["height_m"] = df["height"] / 10
df["weight_kg"] = df["weight"] / 10
df["imc"] = df["weight_kg"] / (df["height_m"] ** 2)

# 6. Guardado del pergamino
df.to_csv("pokemon_final.csv", index=False)
df.to_json("pokemon_final.json", orient="records", indent=4)

print("✅ Archivos guardados:")
print(" - pokemon_final.csv")
print(" - pokemon_final.json")