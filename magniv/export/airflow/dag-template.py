from datetime import datetime

import requests
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {"owner": ownertoreplace, "start_date": datetime(2021, 1, 1)}


def callback_post(callback_type, context):
    """
    It sends a POST request to the callbackhooktoreplace URL with a JSON payload containing the
    callback_type, task_id, run_id, and id

    :param callback_type: The type of callback
    :param context: A dictionary containing the following keys:
    """
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
    """
    It calls the callback_post function with the "success" status and the context object

    :param context: The context object that was passed to the original function
    """
    callback_post("success", context)


def _on_failure(context):
    """
    If the job fails, call the callback_post function with the "failure" status and the context object

    :param context: The context object that is passed to the task
    """
    callback_post("failure", context)


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
        resources=resourcesdicttoreplace,
        startup_timeout_seconds=startuptoreplace,
        on_failure_callback=failuretoreplace,
        on_success_callback=successtoreplace,
    )
