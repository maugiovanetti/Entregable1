import requests
import pandas as pd
from googletrans import Translator
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import execute_values


#Comprueba para todas las provincias de Argentina, temperatura, humedad y una descripcion (En español)

#pip install pandas
#pip install requests
#pip install googletrans==4.0.0-rc1
#pip pipinstall psycopg2
#pip install sqlalchemy

# Configurar la API key de OpenWeatherMap
api_key = "cb3c7af6f8a3112d069b2cd42e3d2651"

# Definir las provincias de Argentina
provincias = ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Tucumán", "Entre Rios", "Salta", "Chaco", "Corrientes", "Misiones", "Santiago del Estero", "San Juan", "San Salvador de Jujuy", "Río Negro", "Formosa", "Neuquén", "Rawson", "San Luis", "Catamarca", "La Rioja", "La Pampa", "Santa Cruz", "Ushuaia"]

# Crear una lista para almacenar los datos del clima de cada provincia
datos_clima = []

#  Crea el traductor
translator = Translator()

# Obtener el clima para cada provincia
for provincia in provincias:
    # Realizar la solicitud a la API de OpenWeatherMap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={provincia}&appid={api_key}&units=metric"
    respuesta = requests.get(url)
    data = respuesta.json()

    # Obtener los datos del clima para la provincia actual
    if "main" in data and "temp" in data["main"] and "humidity" in data["main"] and "weather" in data and len(data["weather"]) > 0:
        temperatura = data["main"]["temp"]
        humedad = data["main"]["humidity"]
        descripcion_ingles = data["weather"][0]["description"]

        # Traducir la descripción del clima al español
        descripcion = translator.translate(descripcion_ingles, src='en', dest='es').text

        # Agregar los datos del clima a la lista
        datos_clima.append([provincia, temperatura, humedad, descripcion])
    else:
        # Agregar valores nulos para la provincia si los datos no están disponibles
        datos_clima.append([provincia, None, None, None])

# Crear un DataFrame de pandas con los datos del clima
tabla_clima = pd.DataFrame(datos_clima, columns=["Provincia", "Temperatura (°C)", "Humedad (%)", "Descripción"])

# Agregar una columna "id" autoincremental
tabla_clima.insert(0, "id", range(1, len(tabla_clima) + 1))

# Establecer la columna "id" como el índice del DataFrame
tabla_clima.set_index("id", inplace=True)

# Mostrar la tabla de clima
#print(tabla_clima)



# Datos de conexión a Amazon Redshift
host = "data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com"
port = 5439
database = "data-engineer-database"
user = "mau_giovanetti_coderhouse"
password = "5K6m1tR3h9"
schema = "mau_giovanetti_coderhouse"  # Nombre del esquema donde se creará la tabla

# Nombre de la tabla y columnas
table_name = "clima_argentina"
column_definitions = '''
    id INTEGER PRIMARY KEY,
    provincia VARCHAR(255),
    temperatura FLOAT,
    humedad INTEGER,
    descripcion VARCHAR(255)
'''

# Establecer la conexión con Redshift
conn = psycopg2.connect(
    host=host,
    port=port,
    database=database,
    user=user,
    password=password
)

# Crear un cursor para ejecutar consultas
cur = conn.cursor()

# Cambiar al esquema deseado
set_schema_query = f'SET search_path TO {schema};'
cur.execute(set_schema_query)

# Consulta SQL para crear la tabla
create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        {column_definitions}
    );
'''

# Ejecutar la consulta para crear la tabla
cur.execute(create_table_query)

# Convertir el DataFrame a una lista de tuplas para la inserción
data = [tuple(row) for row in tabla_clima.values]

# Consulta SQL para la inserción de datos
insert_query = f'''
    INSERT INTO {table_name} (provincia, temperatura, humedad, descripcion)
    VALUES %s;
'''


# Convertir el DataFrame a una lista de tuplas para la inserción
data = [(index,) + tuple(row) for index, row in tabla_clima.iterrows()]

# Consulta SQL para la inserción de datos
insert_query = f'''
    INSERT INTO {table_name} (id, provincia, temperatura, humedad, descripcion)
    VALUES %s;
'''

# Ejecutar la inserción de datos utilizando execute_values para mejorar el rendimiento
execute_values(cur, insert_query, data)



# Confirmar los cambios en la base de datos
conn.commit()

# Cerrar el cursor y la conexión
cur.close()
conn.close()

print("Los datos se han insertado correctamente en la tabla.")