import os
import shutil
import fileinput
import docker
from io import BytesIO
from magniv.utils.utils import _create_cloud_build


def export_to_airflow(task_list, gcp=False, gcp_project_id=None, gcp_dag_folder=None):
    dag_template_filename = "dag-template.py"
    dag_template_directory = "{}/{}".format(
        os.path.dirname(__file__), dag_template_filename
    )
    docker_image_info = []
    for task_info in task_list:
        print("starting task .... ")
        new_filename = "dags/{}/{}.py".format(task_info["owner"], task_info["key"])
        print(new_filename)
        if not os.path.exists("dags/"):
            os.mkdir("dags")
        if not os.path.exists("dags/{}/".format(task_info["owner"])):
            os.mkdir("dags/{}/".format(task_info["owner"]))
        shutil.copyfile(dag_template_directory, new_filename)
        docker_name, path = _create_docker_image(
            task_info["python_version"],
            task_info["requirements_location"],
            task_info["key"],
            gcp=gcp,
            gcp_project_id=gcp_project_id,
        )
        docker_image_info.append((docker_name, path))
        with fileinput.input(new_filename, inplace=True) as f:
            for line in f:
                line = (
                    line.replace("dag_id", "'{}'".format(task_info["key"]))
                    .replace("ownertoreplace", "'{}'".format(task_info["owner"]))
                    .replace("scheduletoreplace", "'{}'".format(task_info["schedule"]))
                    .replace("imagetoreplace", "'{}'".format(docker_name))
                    .replace("filetoreplace", task_info["location"])
                    .replace("functiontoreplace", task_info["name"])
                )
                print(line, end="")
    if gcp:
        _create_cloud_build(docker_image_info, gcp_dag_folder)


def _create_docker_image(
    python_version, requirements, key, gcp=False, gcp_project_id=None
):
    path = "/".join(requirements.split("/")[:-1])
    if not gcp:
        requirements = "requirements.txt"
    dockerfile = """
# syntax=docker/dockerfile:1

FROM python:{}
COPY {} requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
                """.format(
        python_version, requirements
    )
    with open("{}/Dockerfile".format(path), "w") as fo:
        fo.write(dockerfile)
    docker_name = "{}dockerimage".format(key)
    if gcp:
        docker_name = "gcr.io/{}/{}".format(gcp_project_id, docker_name)
    else:
        client = docker.from_env()
        client.images.build(path=path, tag=docker_name)
    return docker_name, path
