from airflow import DAG
from airflow.operators.python_operator import PythonOperator # 기본 Operator. 종류가 많다.

def function1():
  # TODO

def function2():
  # TODO

# 기본 args 생성
default_args = {
  'owner' : 'Hello', # DAGs 메뉴에서 각 DAG들의 Owner 자리에 표시되는 이름
}

# DAG 생성
with DAG(
  dag_id='dag_id' # DAGs 메뉴에서 각 DAG들의 이름으로 표시
  default_args=default_args
  start_date=datetime(2023, 7, 7),
  description='description',
  schedule_interval='* * * * *', # 크론탭 형태
  tag=['article']
) as dag:
  t1 = PythonOperator(
    task_id='function1', // 위에서 작성한 def의 명칭
    python_callable=function1,
    provide_context=True
  )
  t2 = PythonOperator(
    task_id='function2', // 위에서 작성한 def의 명칭
    python_callable=function2,
    provide_context=True
  )


  t1 >> t2 // 실행 순서
