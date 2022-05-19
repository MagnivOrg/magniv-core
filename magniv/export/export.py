from magniv.export.airflow import export_to_airflow
from magniv.utils.utils import _get_tasks_json


def export(gcp=False, gcp_project_id=None, gcp_dag_folder=None):
    task_list = _get_tasks_json("./dump.json")
    export_to_airflow(
        task_list, gcp=gcp, gcp_project_id=gcp_project_id, gcp_dag_folder=gcp_dag_folder
    )
