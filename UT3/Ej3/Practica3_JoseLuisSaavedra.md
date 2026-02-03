# Práctica 3: Extracción de datos en CoinMarketCap

## Objetivo de la práctica

Debes desarrollar un script en Python que realice las siguientes tareas:

### Extracción masiva
- Obtener los datos de las **500 primeras criptomonedas** (esto implicará navegar por varias páginas de resultados).

### Campos obligatorios
Por cada moneda, debes extraer:
- Nombre del activo.
- Símbolo (ej. BTC, ETH).
- Precio actual.
- Market Cap (Capitalización de mercado).
- Volumen de las últimas 24 horas.

### Almacenamiento
- Guardar los resultados en un archivo `cripto_data.csv` utilizando la librería **pandas**.

---

## Guía y pistas para CoinMarketCap

Para completar tu misión con éxito en CoinMarketCap, ten en cuenta las siguientes recomendaciones técnicas:

## 1. La estructura de la tabla

CoinMarketCap presenta la información en una tabla HTML donde cada criptomoneda corresponde a una fila. Analizando la estructura de la página se puede identificar cómo se distribuyen los datos en columnas, lo que permite localizar campos como el nombre o el precio según su posición.

## 2. Identificación por selectores CSS

Debido al uso de clases dinámicas, es más fiable localizar los datos mediante etiquetas HTML concretas. El nombre del activo y su precio suelen encontrarse dentro de etiquetas específicas fácilmente reconocibles por su contenido.

## 3. Gestión de la paginación

La plataforma muestra un número limitado de resultados por página. Para acceder a un conjunto mayor de criptomonedas, es necesario recorrer varias páginas modificando el parámetro de paginación de la URL y controlando la frecuencia de las peticiones.

## 4. Cabeceras de navegación (User-Agent)

Algunos servidores bloquean solicitudes automatizadas. Para evitar este problema, es importante simular una navegación real incluyendo cabeceras adecuadas en las peticiones.

## 5. Limpieza de datos

Los valores obtenidos suelen estar en formato de texto con símbolos y separadores. Antes de almacenarlos o analizarlos, es necesario transformarlos en valores numéricos eliminando caracteres innecesarios.

## Criterios de entrega

- El script debe ejecutarse sin errores.
- El archivo CSV debe contener exactamente las 500 primeras monedas con todas las columnas solicitadas.
- El código debe estar comentado explicando cada sección del proceso.
