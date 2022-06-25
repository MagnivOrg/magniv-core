import json


def _save_to_json(obj, filepath):
    """
    It takes a Python object and a filepath, and saves the object to the filepath as a JSON file

    :param obj: the object to be saved
    :param filepath: The path to the file to save the data to
    """
    with open(filepath, "w") as fo:
        json.dump(obj, fo)


def _get_tasks_json(filepath):
    """
    It opens the file at the given filepath, reads the contents of the file, and returns the contents as
    a Python object

    :param filepath: The path to the JSON file containing the tasks
    :return: A list of dictionaries.
    """
    with open(filepath) as fo:
        task_list = json.load(fo)
    return task_list


def _create_cloud_build(docker_image_info, gcp_dag_folder):
    """
    It creates a cloudbuild.yaml file that will build all the docker images and then sync the dags
    folder to the GCP bucket

    :param docker_image_info: A list of tuples. Each tuple contains the name of the image you want to
    build and the path to the Dockerfile
    :param gcp_dag_folder: The GCP bucket where the DAGs will be stored
    """
    with open("./cloudbuild.yaml", "w") as fo:
        fo.write(
            f"steps:\n- name: gcr.io/cloud-builders/gsutil\n  args:\n    - '-m'\n    - 'rsync'\n    - '-d'\n    - '-r'\n    - 'dags'\n    - '{gcp_dag_folder}'"
        )
        gcp_image_names = []
        for docker_info in docker_image_info:
            gcp_image_name = docker_info[0]
            path = docker_info[1]
            gcp_image_names.append(gcp_image_name)
            fo.write(
                f"\n- name: 'gcr.io/cloud-builders/docker'\n  args: [ 'build', '-t','{gcp_image_name}', '-f', '{path}/Dockerfile', '.' ]"
            )
        fo.write("\nimages: [{}]".format(",".join(f"'{image}'" for image in gcp_image_names)))
