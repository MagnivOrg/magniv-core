from magniv.export.airflow import export_to_airflow
from magniv.utils.utils import _get_tasks_json


def export(
    gcp=False,
    gcp_project_id=None,
    gcp_dag_folder=None,
    callback_hook=None,
    kubernetes_startup_timeout=None,
    env_file_path=None,
):
    """
    It takes a list of tasks and exports them to Airflow

    :param gcp: If you want to export to GCP, set this to True, defaults to False (optional)
    :param gcp_project_id: The GCP project ID where the DAGs will be deployed
    :param gcp_dag_folder: The folder in which the DAGs will be created
    :param callback_hook: A function that will be called after the DAG is exported
    :param kubernetes_startup_timeout: The amount of time to wait for the Kubernetes pod to start up
    :param env_file_path: The path to the environment file
    """
    task_list = _get_tasks_json("./dump.json")
    export_to_airflow(
        task_list,
        gcp=gcp,
        gcp_project_id=gcp_project_id,
        gcp_dag_folder=gcp_dag_folder,
        callback_hook=callback_hook,
        kubernetes_startup_timeout=kubernetes_startup_timeout,
        env_file_path=env_file_path,
    )
