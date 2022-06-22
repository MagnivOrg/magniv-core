import fileinput
import os
import shutil

import docker
from dotenv import dotenv_values

from magniv.utils.utils import _create_cloud_build


def export_to_airflow(
    task_list,
    gcp=False,
    gcp_project_id=None,
    gcp_dag_folder=None,
    callback_hook=None,
    kubernetes_startup_timeout=None,
    env_file_path=None,
):
    """
    It takes a list of tasks, creates a docker image for each task, creates a dag file for each task,
    and then creates a cloud build file to build the docker images.

    :param task_list: a list of dictionaries, each dictionary containing the following keys:
    :param gcp: If you want to use Google Cloud Platform, set this to True, defaults to False (optional)
    :param gcp_project_id: The project id of your GCP project
    :param gcp_dag_folder: The folder where the dag files will be stored
    :param callback_hook: This is the URL of the callback function that will be called when the task is
    completed
    :param kubernetes_startup_timeout: This is the time in seconds that Airflow will wait for the
    Kubernetes pod to start
    :param env_file_path: This is the path to the environment file that you want to use
    """
    dag_template_filename = "dag-template.py"
    dag_template_directory = f"{os.path.dirname(__file__)}/{dag_template_filename}"
    docker_image_info = []
    for task_info in task_list:
        print("starting task .... ")
        new_filename = "dags/{}/{}.py".format(task_info["owner"], task_info["key"])
        print(new_filename)
        if not os.path.exists("dags/"):
            os.mkdir("dags")
        if not os.path.exists(f'dags/{task_info["owner"]}/'):
            os.mkdir(f'dags/{task_info["owner"]}/')
        shutil.copyfile(dag_template_directory, new_filename)
        print("creating docker image ... ")
        docker_name, path = _create_docker_image(
            task_info["python_version"],
            task_info["requirements_location"],
            task_info["key"],
            gcp=gcp,
            gcp_project_id=gcp_project_id,
            env_file_path=env_file_path,
        )
        print("docker image created!")
        docker_image_info.append((docker_name, path))
        print("creating dag ... ")
        with fileinput.input(new_filename, inplace=True) as f:
            for line in f:
                line = (
                    line.replace("dag_id", f"""'{task_info["key"]}'""")
                    .replace("ownertoreplace", f"""'{task_info["owner"]}'""")
                    .replace("scheduletoreplace", f"""'{task_info["schedule"]}'""")
                    .replace("imagetoreplace", f"'{docker_name}'")
                    .replace("filetoreplace", task_info["location"])
                    .replace("functiontoreplace", task_info["name"])
                    .replace(
                        "callbackhooktoreplace",
                        f"'{callback_hook}'" if callback_hook is not None else "None",
                    )
                    .replace(
                        "successtoreplace", "_on_success" if callback_hook is not None else "None"
                    )
                    .replace(
                        "failuretoreplace", "_on_failure" if callback_hook is not None else "None"
                    )
                    .replace("startuptoreplace", str(kubernetes_startup_timeout))
                )

                print(line, end="")
        print("dag created!")
    if gcp:
        _create_cloud_build(docker_image_info, gcp_dag_folder)


def _create_docker_image(
    python_version,
    requirements,
    key,
    gcp=False,
    gcp_project_id=None,
    env_file_path=None,
):
    """
    It creates a Dockerfile in the same directory as the requirements.txt file, and then builds a docker
    image from that Dockerfile

    :param python_version: The version of python you want to use
    :param requirements: The path to the requirements.txt file
    :param key: This is the name of the function key. It's used to name the docker image
    :param gcp: If you're using GCP, set this to True, defaults to False (optional)
    :param gcp_project_id: The ID of the GCP project you want to use
    :param env_file_path: The path to the .env file that contains the environment variables that you
    want to pass to the Docker container
    :return: The docker image name and the path to the dockerfile
    """
    path = "/".join(requirements.split("/")[:-1])
    if not gcp:
        requirements = "requirements.txt"
    environment_arguments = ""
    if env_file_path is not None:
        env_values_dict = dotenv_values(env_file_path)
        environment_arguments = "\n".join(
            [f'ENV {key}="{env_values_dict[key]}"' for key in env_values_dict]
        )
    dockerfile = """
# syntax=docker/dockerfile:1

FROM python:{}
COPY {} requirements.txt
{}
RUN pip3 install -r requirements.txt

COPY . .
                """.format(
        python_version, requirements, environment_arguments
    )
    with open(f"{path}/Dockerfile", "w") as fo:
        fo.write(dockerfile)
    docker_name = f"{key}dockerimage"
    if gcp:
        docker_name = f"gcr.io/{gcp_project_id}/{docker_name}"
    else:
        client = docker.from_env()
        client.images.build(path=path, tag=docker_name)
    return docker_name, path
