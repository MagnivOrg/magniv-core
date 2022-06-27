from magniv.core import task
from datetime import datetime

@task(schedule="@hourly", description='Hello world, printing the time')
def hello_world():
	print("Hello world, the time is {}".format(datetime.now()))

def dummy_task():
    print("This is a dummy task")
    return True

if __name__ == '__main__':
	hello_world()