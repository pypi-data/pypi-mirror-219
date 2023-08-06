import json
from jsonpath_ng.ext.parser import parse

from airflow.providers.amazon.aws.sensors.sqs import SqsSensor
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

from rcplus_alloy_common.airflow.decorators import alloyize


@alloyize
class AlloySqsSensor(SqsSensor):
    """Alloy SqsSensor class with default arguments injected with on_failure_callback.

    NOTE: we use jsonpath_ng.ext.parser.parse (instead of jsonpath_ng.parse) in order to support xpath filters
    """

    def filter_messages_jsonpath(self, messages):
        # NOTE: we use from jsonpath_ng.ext.parser in order to support the filter
        jsonpath_expr = parse(self.message_filtering_config)
        filtered_messages = []
        for message in messages:
            body = message["Body"]
            # Body is a string, deserialize to an object and then parse
            body = json.loads(body)
            results = jsonpath_expr.find(body)
            if not results:
                continue
            if self.message_filtering_match_values is None:
                filtered_messages.append(message)
                continue
            for result in results:
                if result.value in self.message_filtering_match_values:
                    filtered_messages.append(message)
                    break
        self.log.info(f"Filtered {len(messages)} messages to {len(filtered_messages)} messages: {filtered_messages}")
        return filtered_messages


class S3NoKeySensor(S3KeySensor):
    """
    Customize the default S3KeySensor to check files the way we need.
    If the given S3 key (or list of keys) is missed then return True.

    The `wildcard_match` option is ignored.
    """

    def __init__(self, *args, lock_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock_id = lock_id or self.dag_id

    def _check_key(self, key):
        self.log.info(f"Poking for key `s3://{self.bucket_name}/{key}`")

        s3_hook = self.get_hook()
        s3_object = s3_hook.head_object(key, self.bucket_name)
        if s3_object is None:
            return True

        # The S3 based locks can be re-entrant locks, so lock owners can ignore them in case of a failure etc.
        # The ownership is detected by lock id value.
        lock_id = s3_hook.read_key(key, self.bucket_name)
        if lock_id == self.lock_id:
            self.log.info(f"Re-enter lock `s3://{self.bucket_name}/{key}` because its lock id is `{self.lock_id}`")
            return True

        return False


@alloyize
class AlloyS3NoKeySensor(S3NoKeySensor):
    """Alloy S3NoKeySensor"""
