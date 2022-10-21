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

GET_DECORATED_NODES_FILE = """from datetime import datetime

import magniv
from magniv.core import task
from magniv import core as mc


@magniv.core.task(schedule="@hourly", description="Hello world, printing the time", key="goodbye_world_1")
def hello_world():
    print(f"Hello world, the time is {datetime.now()}")

@task(schedule="@daily", description="Hello world, printing a second time", key="goodbye_world_2")
def hello_world_2():
    print(f"Hello world, the time is {datetime.now()}")

@mc.task(schedule="@daily", description="Hello world, printing a third time", key="goodbye_world_3")
def hello_world_3():
    print(f"Hello world, the time is {datetime.now()}")

@dummydecorator
def dummy_task():
    print("This is a dummy task")
    return True

def dummy_task_2():
    print("This is a dummy task")
    return True

if __name__ == "__main__":
    hello_world()
"""
