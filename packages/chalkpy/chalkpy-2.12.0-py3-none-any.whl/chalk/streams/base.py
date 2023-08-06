from typing import Any, Union


class StreamSource:
    """Base class for all stream sources generate from `@stream`."""

    def _config_to_json(self) -> Any:
        ...

    @property
    def streaming_type(self) -> str:
        """e.g. 'kafka' or 'kinesis'"""
        raise NotImplemented()

    @property
    def dlq_name(self) -> Union[str, None]:
        """stream name for kinesis, topic for kafka"""
        raise NotImplemented()
