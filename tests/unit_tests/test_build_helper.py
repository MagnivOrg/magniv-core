from datetime import datetime

from magniv.core import task


@task(schedule="@hourly", description="Hello world, printing the time")
def hello_world():
    print(f"Hello world, the time is {datetime.now()}")


def dummy_task():
    print("This is a dummy task")
    return True


if __name__ == "__main__":
    hello_world()
