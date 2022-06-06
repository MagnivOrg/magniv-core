from datetime import datetime

import requests
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {"owner": ownertoreplace, "start_date": datetime.now()}


def callback_post(callback_type, context):
    requests.post(
        callbackhooktoreplace,
        json={
            "callback_type": callback_type,
            "task_id": context["task"].task_id,
            "run_id": context["run_id"],
            "id": dag_id,
        },
    )


def _on_success(context):
    callback_post("success", context)


def _on_failure(context):
    callback_post("failure", context)


dag = DAG(
    dag_id,
    schedule_interval=scheduletoreplace,
    default_args=default_args,
    catchup=False,
    on_success_callback=successtoreplace,
    on_failure_callback=failuretoreplace,
)

with dag:
    t1 = KubernetesPodOperator(
        task_id="kubernetes_pod",
        name="kubernetes_pod",
        namespace="default",
        image=imagetoreplace,
        cmds=["magniv-cli", "run", "filetoreplace", "functiontoreplace"],
        on_failure_callback=failuretoreplace,
        on_success_callback=successtoreplace,
    )
