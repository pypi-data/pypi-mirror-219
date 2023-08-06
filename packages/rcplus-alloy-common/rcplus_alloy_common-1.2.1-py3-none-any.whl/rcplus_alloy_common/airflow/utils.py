import os
import sys

import yaml

from rcplus_alloy_common.airflow.observability import slack_alert_on_retry, slack_alert_on_failure


class AlloyProject():
    """Load Alloy project configuration.

    The convention is to put the project.yml in the same directory as the dag script.
    """
    def __init__(self, depth=2) -> None:
        self._depth = depth
        self.config = self._load_project_config()

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value: int):
        self._depth = value
        self.config = self._load_project_config()

    def __getitem__(self, key):
        return self.config[key]

    def __contains__(self, key):
        return key in self.config

    def get(self, key, default=None):
        return self.config.get(key, default)

    def _load_project_config(self):
        back = sys._getframe(self.depth)  # pylint: disable=protected-access
        fileloc = back.f_code.co_filename if back else ""
        config_filepath = os.path.join(os.path.dirname(fileloc), "project.yml")

        with open(config_filepath) as f:
            project = yaml.safe_load(f)
        return project

    def get_templated_var(self, variable_name, prefix=None):
        if prefix is None:
            prefix = self["software_component"]
        return f"{{{{ var.value.get('{prefix}/{variable_name}') }}}}"


def set_default_callbacks(default_args):
    """Set default callbacks for tasks

    TODO: does the order matters?
    """
    if "on_retry_callback" not in default_args:
        default_args["on_retry_callback"] = slack_alert_on_retry
    elif isinstance(default_args["on_retry_callback"], list):
        default_args["on_retry_callback"] = (
            [x for x in default_args["on_retry_callback"] if x is not slack_alert_on_retry]
        )
        default_args["on_retry_callback"] = default_args["on_retry_callback"] + [slack_alert_on_retry]
    else:
        if default_args["on_retry_callback"] is not slack_alert_on_retry:
            default_args["on_retry_callback"] = [default_args["on_retry_callback"], slack_alert_on_retry]

    if "on_failure_callback" not in default_args:
        default_args["on_failure_callback"] = slack_alert_on_failure
    elif isinstance(default_args["on_failure_callback"], list):
        default_args["on_failure_callback"] = (
            [x for x in default_args["on_failure_callback"] if x is not slack_alert_on_failure]
        )
        default_args["on_failure_callback"] = default_args["on_failure_callback"] + [slack_alert_on_failure]
    else:
        if default_args["on_failure_callback"] is not slack_alert_on_failure:
            default_args["on_failure_callback"] = [default_args["on_failure_callback"], slack_alert_on_failure]
    return default_args
