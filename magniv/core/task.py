import re
from functools import update_wrapper
from typing import Callable, Dict

from croniter import CroniterBadCronError, CroniterBadDateError, CroniterNotAlphaError, croniter


class Task:
    """

    This class contains all the relevant information for each task, it is used as a decorator placed around functions
    that are to be deployed.

    :param function: the function that is being decorated
    :param schedule: the cron schedule that this function will be scheduled with
    :param resources: the resource requirements for this function
    :param description: description of the function, to be used for the auto generated documentation
    :param key: the unique key that will reference the function, default is the function of the name
    """

    KEY_PATTERN = r"^[\w\-.]+$"

    def __init__(self, function, schedule=None, resources=None, description=None, key=None) -> None:
        if schedule is None:
            raise ValueError("schedule must be provided")
        if not self._is_valid_schedule(schedule):
            raise ValueError(f"{schedule} is not a valid cron schedule")
        self.schedule = schedule
        self.resources = resources
        self.description = description
        self.function = function
        self.name = function.__name__
        self.key = key
        if key is None:
            self.key = self.name
        elif not self._is_valid_key(key):
            raise ValueError(
                f"{key} is not a valid key, the key can only contain alphanumeric characters, -, _, . and space."
            )

        update_wrapper(self, function)

    def as_dict(self) -> dict:
        return {
            "schedule": self.schedule,
            "description": self.description,
            "name": self.name,
            "key": self.key,
        }

    def __call__(self, *args, **kwds) -> Callable:
        return self.function(*args, **kwds)

    def _is_valid_schedule(self, schedule) -> bool:
        """
        It returns `True` if the given `schedule` is a valid cron expression, and `False` otherwise
        Based on whatever Airflow accepts as a valid cron expression

        :param schedule: The cron schedule for the task
        :return: A boolean value.
        """
        try:
            croniter(schedule)
            return True
        except (
            CroniterBadCronError,
            CroniterBadDateError,
            CroniterNotAlphaError,
        ) as cron_e:
            return False
        return bool(re.match(Task.CRON_PATTERN, schedule))

    def _is_valid_key(self, key) -> bool:
        """
        It returns `True` if the given `key` matches the regular expression `Task.KEY_PATTERN`, and `False`
        otherwise

        :param key: The key of the task
        :return: A boolean value.
        """
        return bool(re.match(Task.KEY_PATTERN, key))
    
    def _is_valid_resources(self, resources) -> Dict[str, str]:
        """
        TODO: add functionality to sanitize inputs for resource requests
        """
        return resources


def task(_func=None, *, schedule=None, resources=None, description=None, key=None) -> Callable:
    """
    If they pass in a function, then we raise an error. If they dont pass in a function, then we return
    a wrapper function that takes a function as an argument

    :param _func: This is the function that is being wrapped
    :param schedule: This is the schedule that the task will run on. It can be a cron string, or a
    datetime.timedelta object
    :param resources: A dictionary describing the resource requirements for this task
    :param description: A description of the task
    :param key: This is the name of the task key. It is used to identify the task in the database
    :return: A function that takes in a function and returns a task instance.
    """
    if _func is not None:  # this means they did not pass in any arguments like @magniv
        # The reason we do this here is bc in the case they dont pass arguments we dont need the extra wrapper below.
        raise ValueError("You must use arguments with magniv, it can not be called alone")

    def wrapper(function):
        return Task(function, schedule=schedule, resources=resources, description=description, key=key)

    return wrapper
