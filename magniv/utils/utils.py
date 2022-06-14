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


def _get_function_from_json(key, filepath):
    """
    It takes a key and a filepath, and returns the location and name of the function that corresponds to
    that key
    
    :param key: the key of the task you want to run
    :param filepath: the path to the json file that contains the function information
    :return: The location and name of the function
    """
    f = open(filepath)
    task_info_list = json.load(f)
    for task in task_info_list:
        if task["key"] == key:
            break
    return task["location"], task["name"]


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
            "steps:\n- name: gcr.io/cloud-builders/gsutil\n  args:\n    - '-m'\n    - 'rsync'\n    - '-d'\n    - '-r'\n    - 'dags'\n    - '{}'".format(
                gcp_dag_folder
            )
        )
        gcp_image_names = []
        for docker_info in docker_image_info:
            gcp_image_name = docker_info[0]
            path = docker_info[1]
            gcp_image_names.append(gcp_image_name)
            fo.write(
                "\n- name: 'gcr.io/cloud-builders/docker'\n  args: [ 'build', '-t','{}', '-f', '{}/Dockerfile', '.' ]".format(
                    gcp_image_name, path
                )
            )
        fo.write("\nimages: [{}]".format(",".join(f"'{image}'" for image in gcp_image_names)))
