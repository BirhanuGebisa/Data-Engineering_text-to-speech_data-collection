
from datetime import datetime, date
import json
import pandas as pd
import consumer
from kafka import KafkaConsumer
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import sys
import os
sys.path.append(f'{os.getcwd()}/api/')
from kafka import KafkaConsumer
import consumer
import pandas as pd
import json
from datetime import datetime,date
now = datetime.now()
# print (now.strftime("%Y%m%d%H%M%S"))
suf=now.strftime("%Y%m%d%H%M%S")
TIME_OUT=20000
def consume_text(ti):
    all_messages=consumer.consume("g1-text", "g1-t", time_out=TIME_OUT)
    print(all_messages)
    ti.xcom_push(key="raw",value=all_messages)

def consume_audio(ti):
    all_audio=consumer.consume("g1-audio", "g1-a", time_out=TIME_OUT)
    ti.xcom_push(key="raw_a",value=all_audio)

def combine_save(ti):
    txt_json=ti.xcom_pull(key="raw",task_ids='corpus_consumer')
    aud_json=ti.xcom_pull(key="raw_a",task_ids='audio_consumer')

    if(txt_json != []):
        
        df=pd.DataFrame.from_dict(json.loads(txt_json))
        df.rename(columns={"1":"id","0":"headline"},inplace=True)
        df.to_csv(f"{os.getcwd()}/dlk/txt_{suf}.csv")

    if(aud_json != []):
        df1=pd.DataFrame.from_dict(json.loads(aud_json))
        df1.to_csv(f"{os.getcwd()}/dlk/aud_{suf}.csv")

default_args = {
    'owner': 'G-1',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

with DAG(
    default_args=default_args,
    dag_id ='raw_data_handler',
    description = "Accepts raw data and store to unprocessed storage",
    start_date = datetime(2022,10,4,10),
    # schedule_interval = timedelta(minutes=5)
    schedule_interval = "@daily"
) as dag:
#A task bash operator = runs bash command, python operator = runs python code
    
    read_data = PythonOperator(
        task_id='corpus_consumer',
        python_callable = consume_text,
    )

    read_aud_data = PythonOperator(
        task_id='audio_consumer',
        python_callable = consume_audio,
    )

    combine_save_data = PythonOperator(
        task_id='combine_save_data',
        python_callable = combine_save,
    ) 
    
    
    [read_data,read_aud_data] >> combine_save_data