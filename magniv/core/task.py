import re
from functools import update_wrapper
from typing import Callable


class Task:
    """

    This class contains all the relevant information for each task, it is used as a decorator placed around functions
    that are to be deployed.

    :param function: the function that is being decorated
    :param schedule: the cron schedule that this function will be scheduled with
    :param description: description of the function, to be used for the auto generated documentation
    :param key: the unique key that will reference the function, default is the function of the name
    """

    CRON_PATTERN = r"(^((\*\/)?([1-5]?[0-9])((\,|\-|\/)\d+)*|\*)\s((\*\/)?((2[0-3]|1[0-9]|[0-9]))((\,|\-|\/)\d+)*|\*)\s((\*\/)?([1-9]|[12][0-9]|3[01])((\,|\-|\/)\d+)*|\*)\s((\*\/)?([1-9]|1[0-2])((\,|\-|\/)\d+)*|\*)\s((\*\/)?[0-6]((\,|\-|\/)\d+)*|\*)$)|@(annually|yearly|monthly|weekly|daily|hourly|reboot)"
    KEY_PATTERN = r"^[\w\-.]+$"

    def __init__(self, function, schedule=None, description=None, key=None) -> None:
        if schedule is None:
            raise ValueError("Schedule must be provided")
        if not self._is_valid_schedule(schedule):
            raise ValueError(f"{schedule} is not a valid cron schedule")
        self.schedule = schedule
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

    def __call__(self, *args, **kwds) -> Callable:
        return self.function(*args, **kwds)

    def _is_valid_schedule(self, schedule) -> bool:
        """
        It returns `True` if the given `schedule` is a valid cron expression, and `False` otherwise

        :param schedule: The cron schedule for the task
        :return: A boolean value.
        """
        return bool(re.match(Task.CRON_PATTERN, schedule))

    def _is_valid_key(self, key) -> bool:
        """
        It returns `True` if the given `key` matches the regular expression `Task.KEY_PATTERN`, and `False`
        otherwise

        :param key: The key of the task
        :return: A boolean value.
        """
        return bool(re.match(Task.KEY_PATTERN, key))


def task(_func=None, *, schedule=None, description=None, key=None) -> Callable:
    """
    If they pass in a function, then we raise an error. If they dont pass in a function, then we return
    a wrapper function that takes a function as an argument

    :param _func: This is the function that is being wrapped
    :param schedule: This is the schedule that the task will run on. It can be a cron string, or a
    datetime.timedelta object
    :param description: A description of the task
    :param key: This is the name of the task key. It is used to identify the task in the database
    :return: A function that takes in a function and returns a task instance.
    """
    if _func is not None:  # this means they did not pass in any arguments like @magniv
        # The reason we do this here is bc in the case they dont pass arguments we dont need the extra wrapper below.
        raise ValueError("You must use arguments with magniv, it can not be called alone")

    def wrapper(function):
        return Task(function, schedule=schedule, description=description, key=key)

    return wrapper
