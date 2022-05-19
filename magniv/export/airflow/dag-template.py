from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from datetime import datetime

default_args = {"owner": ownertoreplace, "start_date": datetime.now()}

dag = DAG(
    dag_id,
    schedule_interval=scheduletoreplace,
    default_args=default_args,
    catchup=False,
)

with dag:
    t1 = KubernetesPodOperator(
        task_id="kubernetes_pod",
        name="kubernetes_pod",
        namespace="default",
        image=imagetoreplace,
        cmds=["magniv-cli", "run", "filetoreplace", "functiontoreplace"],
    )
