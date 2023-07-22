## 설치 과정
이하 명령어들을 입력한다.

**공식문서 참조**
https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html
2023-07-06 기준
```
pip install "apache-airflow[celery]==2.6.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.2/constraints-3.7.txt"
```

>> Airflow를 pip로 설치한다.
```
airflow db init
```

>> DB 초기화
```
airflow user create -username admin -firstname admin -lastname admin -role Admin -email email@email.com -password admin
```

>> “–role Admin” 부분에서 관리자 권한을 부여, admin 유저 생성
```
export AIRFLOW_HOME=~/airflow
```

>> 환경변수 설정
```
airflow webserver -p 8080 // 웹서버 실행
airflow scheduler // Dags 실행
```

>> 이 두 명령어를 서로 다른 쉘에서 실행


## 활용 방법
- 위 설치 과정에서 문제가 없었다면 리눅스 우분투의 경우 Home 경로에 airflow라는 폴더가 만들어진다. 그 폴더 내부에 ‘dags’라는 이름의 폴더를 직접 생성하고, 그 안에 DAG 문법에 맞는 Python 파일을 생성하면 Airflow가 인식한다.
- 이어 웹서버에 접속하게 되면 상단 메뉴에 “DAGs”라는 메뉴를 볼 수 있다. 그 메뉴를 클릭하면 최초 모든 Dag들이 Paused 상태인 것을 볼 수 있는데, 작성한 DAG의 이름을 찾아 실행 버튼을 눌러주면 Active 상태로 바뀌게 된다.
- Dag 하나를 클릭해 상세화면으로 넘어가면 또 여러 메뉴를 볼 수 있는데, 기본은 Grid라는 탭으로 Dag 실행 내역을 막대 그래프 형태로 보여준다. 실행 시간을 보여주는 막대 그래프 아래에 Dag 내부에서 실행한 함수들이 정사각형으로 나열되어 있고, 만약 Log를 보고 싶다면 그 정사각형을 클릭한 후 그래프 우측에 떠오르는 탭들 중 Log 탭을 클릭하면 열람할 수 있다.
- Log는 “airflow scheduler”를 실행한 쉘에서도 볼 수 있지만 해당 쉘에서는 print()로 출력한 내역 등은 볼 수 없는 단점이 있는 반면 위 방법으로 웹서버 상에서 볼 수 있는 Log는 그러한 print() 출력들도 기록된다는 장점이 있다.
