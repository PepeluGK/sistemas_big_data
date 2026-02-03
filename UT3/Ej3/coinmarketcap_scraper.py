import requests
import pandas as pd
import time

# URL de la API interna que usa CoinMarketCap para su tabla
API_URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start={}&limit=100&sortBy=market_cap&sortType=desc&convert=USD"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

data_total = []

for start in range(1, 501, 100):
    print(f"Obteniendo monedas desde la {start} hasta la {start + 99}...")
    
    try:
        response = requests.get(API_URL.format(start), headers=HEADERS)
        json_data = response.json()
        # Navegamos por el JSON para llegar a la lista de criptos
        crypto_list = json_data['data']['cryptoCurrencyList']

        for crypto in crypto_list:
            # Extraemos los campos directamente del JSON
            nombre = crypto['name']
            simbolo = crypto['symbol']
            
            # Los valores numéricos vienen en una lista de 'quotes'
            quote = crypto['quotes'][0] # USD suele ser el primero
            precio = quote['price']
            market_cap = quote['marketCap']
            volumen = quote['volume24h']

            data_total.append({
                'Nombre': nombre,
                'Símbolo': simbolo,
                'Precio': precio,
                'Market Cap': market_cap,
                'Volumen (24h)': volumen
            })
            
    except Exception as e:
        print(f"Error en bloque {start}: {e}")
    
    time.sleep(1) # Pausa mínima

# Convertir a DataFrame y guardar
df = pd.DataFrame(data_total).head(500)
df.to_csv('cripto_data.csv', index=False, encoding='utf-8')

print(f"\n¡Conseguido! {len(df)} criptomonedas guardadas en 'cripto_data.csv'.")