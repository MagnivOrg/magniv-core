import json


def _save_to_json(obj, filepath):
    with open(filepath, "w") as fo:
        json.dump(obj, fo)


def _get_tasks_json(filepath):
    with open(filepath) as fo:
        task_list = json.load(fo)
    return task_list


def _get_function_from_json(key, filepath):
    f = open(filepath)
    task_info_list = json.load(f)
    for task in task_info_list:
        if task["key"] == key:
            break
    return task["location"], task["name"]


def _create_cloud_build(docker_image_info, gcp_dag_folder):
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
