# Airflow
### Gómez Aldrete Luis Ignacio
### 216588253
#
Para esta actividad se desarrolló un ejemplo del uso de *Airflow*, un *workflow manager* como *Prefect*. Antes que nada, *Airflow* funciona exclusivamente bajo entornos *Linux*, esto quiso decir que se tuvo que hacer uso de la herramienta WSL (*"Windows Subsystem for Linux"*) de *Windows* para trabajar con *Airflow* sin recurrir a máquinas virtuales.

Esta herramienta se tiene que habilitar desde el panel de control en la sección de *"Turn Windows features on or off"*.

<img width="450" height="375" src=https://user-images.githubusercontent.com/80866790/224532385-e41e2927-d330-4485-9f11-9551548527a3.png>

Después se tiene que reinciar la máquina e instalar una distribución de Linux que sea soportada por *WSL*, en este caso opte por usar *Ubuntu* 22.04.

Ya dentro de una terminal de *Linux*, se usaron los siguientes comandos para instalar *Python*, un entorno virtual de *Python* y *Airflow*.
```cmd
sudo apt install python3-pip
sudo apt install python3-virtualenv
pip install apache-airflow
```

Después se realizó la configuración de *Airflow*, generando su base de datos y el usuario Admin que haría uso de los *DAGs* que se implementaron.
```cmd
airflow db init
airflow users create --username nachog --firstname nacho --lastname gomez --role Admin --password admin --email luis.gomez5882@alumnos.udg.mx
airflow webserver --port 8080
```

Y una vez ejecutados estos comandos se accedió desde la dirección ```localhost:8080``` a *Airflow* con las credenciales que se registraron.

<img width="450" height="500" src=https://user-images.githubusercontent.com/80866790/224532961-475eb513-449e-48d9-8f76-1c338305e3c1.png>

El DAG que se realizó fue muy sencillo, este se encargaba de informar sobre el clima de Nueva York cada hora (por cuestiones del ejemplo se configuró a un horario de cada 5 minutos).

```python
from datetime import datetime, timedelta
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG
dag = DAG(
    'weather_dag',
    default_args=default_args,
    description='A DAG to get the weather prediction for the day',
    schedule=timedelta(minutes=10)
)

# Define a function to be called by the PythonOperator
def get_weather_prediction():
    # Set the API key and the city
    api_key = '(key_omitida)'
    city = 'New York'
    # Set the URL for the API request
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    # Make the API request
    response = requests.get(url)
    data = response.json()
    # Extract the weather information
    temperature = data['main']['temp']
    description = data['weather'][0]['description']
    # Print the weather information
    print(f'The weather in {city} today is {description} with a temperature of {temperature} degrees Celsius.')

# Define the task to be run by the DAG
task = PythonOperator(
    task_id='get_weather_prediction',
    python_callable=get_weather_prediction,
    dag=dag
```

Este *DAG* usaba una petición a la API de [OpenWeatherMap](https://openweathermap.org/api) para obtener información del clima de una ciudad en específco, en este caso Nueva York.

La manera de ver la información obtenida por el *DAG* era entrando a este desde *AirFlow*, buscando la *task*: "*get_weather_prediction*" y entrando a sus *logs*.

<img width="500" heigth="600" src=https://user-images.githubusercontent.com/80866790/224533673-5d16e186-108c-4146-a303-4773e23912ec.png>

<img width="1000" height="400" src=https://user-images.githubusercontent.com/80866790/224533434-6483a2cb-37d7-42d9-971b-4d40841fc731.png>

<img width="1000" heigth="100" src=https://user-images.githubusercontent.com/80866790/224533458-1d863fd7-a065-42fc-9ae8-007fbd991acf.png>

Por si las imágenes anteriores no son lo suficientemente claras, aquí una transcripción de la información:
```cmd
INFO - The weather in New York today is few clouds with a temperature of 1.38 degrees Celsius.
```

### Conclusión
Conseguir el entorno necesario para usar *AirFlow* fue difícil, pero resultó ser una experiencia de aprendizaje pues logré montar un subsistema *Linux*, además de aprender varios comandos de su terminar que me permitieron completar el ejemplo de este *workflow manager*. 

Sin embargo, una vez configurado el entorno y realizado el ejemplo, puedo decir que el uso de Airflow es muy útil para programar, monitorear y automatizar tareas complejas y repetitivas en un entorno de datos, pues proporciona una plataforma flexible y escalable para crear y ejecutar flujos de trabajo complejos, lo que permite a los usuarios definir, programar y monitorear fácilmente tareas complejas en un entorno centralizado.
