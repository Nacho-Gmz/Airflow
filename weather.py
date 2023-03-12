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