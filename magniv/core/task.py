import re
from functools import update_wrapper
from typing import Callable, Dict
import ast

from croniter import CroniterBadCronError, CroniterBadDateError, CroniterNotAlphaError, croniter

task_kwargs = {
    "on_success": {"ast_type": ast.List, "readable": "list[str]"},
    "resources": {"ast_type": ast.Dict, "readable": "dict"},
    "key": {"ast_type": ast.Constant, "readable": "str"},
    "schedule": {"ast_type": ast.Constant, "readable": "str"},
    "enable_webhook_trigger": {"ast_type": ast.Constant, "readable": "str"},
    "description": {"ast_type": ast.Constant, "readable": "str"},
}

class Task:
    """

    This class contains all the relevant information for each task, it is used as a decorator placed around functions
    that are to be deployed.

    :param function: the function that is being decorated
    :param schedule: the cron-style schedule interval that determines when this function runs
    :param enable_webhook_trigger: boolean flag to enable task being triggered through webhook
    :param resources: the cpu and memory requirements for this function
    :param description: description of the function, to be used for the auto generated documentation
    :param key: the unique key that will reference the function, default is the function of the name
    :param on_success: list of downstream task keys that are triggered after this task's successful completion. Adding multiple tasks to this list will add multiple downstream calls.
    """

    KEY_PATTERN = r"^[\w\-.]+$"

    def __init__(
        self,
        function,
        schedule=None,
        enable_webhook_trigger=False,
        resources=None,
        description=None,
        key=None,
        on_success=None
    ) -> None:
        if schedule is not None and not self._is_valid_schedule(schedule):
            raise ValueError(f"{schedule} is not a valid cron schedule")
        self.schedule = schedule
        self.enable_webhook_trigger = enable_webhook_trigger
        self.resources = self._make_valid_resources(resources)
        self.description = description
        self.function = function
        self.name = function.__name__
        self.key = key if key else self.name
        if key and not self._is_valid_key(key):
            raise ValueError(
                f"{key} is not a valid key, the key can only contain alphanumeric characters, -, _, . and space."
            )
        self.on_success = on_success if on_success else []

        update_wrapper(self, function)

    def as_dict(self) -> dict:
        return {
            "schedule": self.schedule,
            "enable_webhook_trigger": self.enable_webhook_trigger,
            "resources": self.resources,
            "description": self.description,
            "name": self.name,
            "key": self.key,
            "on_success": self.on_success,
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

    def _make_valid_resources(self, resources) -> Dict[str, str]:
        """
        Takes in a resources dictionary with generic parameters and converts it to the appropriate syntax
        for our infrastructure
        #TODO: enforce reasonable limits for quantity of resources
        :param key: The generic resources dict from the task decorator
        :return: A dict with correct syntax
        """
        clean_dict = {}
        if resources is None:
            return resources
        valid_resources = set(["cpu", "memory"])
        invalid_resources = set([r.lower() for r in resources.keys()]) - valid_resources
        if len(invalid_resources) > 0:
            raise KeyError(
                f"{invalid_resources} are not valid resources for a task. Valid resources are {valid_resources}"
            )
        if "cpu" in resources.keys():
            clean_dict["limit_cpu"] = resources["cpu"]
        if "memory" in resources.keys():
            clean_dict["limit_memory"] = resources["memory"]
        return clean_dict

def task(
    _func=None,
    *,
    schedule=None,
    enable_webhook_trigger=False,
    resources=None,
    description=None,
    key=None,
    on_success=None,
) -> Callable:
    """
    If they pass in a function, then we raise an error. If they dont pass in a function, then we return
    a wrapper function that takes a function as an argument

    :param _func: This is the function that is being wrapped
    :param schedule: This is the schedule that the task will run on. It can be a cron string, or a
    datetime.timedelta object, or None
    :param enable_webhook_trigger: Specifices whether this task can be triggered via webhook (see dashboard for webhook URL)
    :param resources: The cpu and memory requirements for this function
    :param description: A description of the task
    :param key: This is the name of the task key. It is used to identify the task in the database
    :param on_success: This is a list of downstream task keys (usually the @task-decorated-function's name) that 
    are triggered by this task on successful completion. Adding multiple tasks to this list will add multiple downstream triggers. (list[str])
    :return: A function that takes in a function and returns a task instance.
    """
    if _func is not None:  # this means they did not pass in any arguments like @magniv
        # The reason we do this here is bc in the case they dont pass arguments we dont need the extra wrapper below.
        raise ValueError("You must use arguments with magniv, it can not be called alone")

    def wrapper(function):
        return Task(
            function,
            schedule=schedule,
            enable_webhook_trigger=enable_webhook_trigger,
            resources=resources,
            description=description,
            key=key,
            on_success=on_success
        )

    return wrapper
