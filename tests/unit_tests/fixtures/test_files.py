INVALID_KWARG_FILE = """from datetime import datetime

from magniv.core import task

@task(schedule="@daily", bad=True)
def task_a():
    print("I")


if __name__ == "__main__":
    hello_world()
"""

INVALID_TASK_KEY_FILE = """from datetime import datetime

from magniv.core import task

@task(schedule="@daily", on_success=['task_b', 'bad_key'])
def task_a():
    print("I")

@task()
def task_b():
    print("i'm only triggered by task A")

@task(key="task_c")
def bad_key():
    print("i'm only triggered by task A")


if __name__ == "__main__":
    hello_world()
"""

INVALID_TRIGGER_FILE = """from datetime import datetime

from magniv.core import task

trigger_lst = ['task_b']

@task(schedule="@daily", _on_success=trigger_lst)
def task_a():
    print("I")

@task()
def task_b():
    print("i'm only triggered by task A")


if __name__ == "__main__":
    hello_world()
"""
