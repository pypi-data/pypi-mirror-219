from typing import Any, List, Optional, Union

from pydantic import BaseModel

from chalk.streams.base import StreamSource
from chalk.utils.duration import Duration


class KinesisSource(StreamSource, BaseModel, frozen=True):
    stream_name: Optional[Union[str, List[str]]] = None
    """The ARN of your stream"""

    stream_arn: Optional[Union[str, List[str]]] = None
    """The ARN of your stream"""

    name: Optional[str] = None
    """
    The name of the integration, as configured in your Chalk Dashboard.
    """

    late_arrival_deadline: Duration = "infinity"
    """
    Messages older than this deadline will not be processed.
    """

    dead_letter_queue_stream_arn: Optional[str] = None
    """
    Kinesis stream ARN to send messages when message processing fails
    """

    aws_access_key_id: Optional[str] = None
    """
    AWS access key id credential
    """

    aws_secret_access_key: Optional[str] = None
    """
    AWS secret access key credential
    """

    aws_session_token: Optional[str] = None
    """
    AWS access key id credential
    """

    region_name: Optional[str] = None
    """
    AWS region string, e.g. "us-east-2"
    """

    endpoint_url: Optional[str] = None
    """
    optional endpoint to hit Kinesis server
    """

    def __init__(
        self,
        *,
        stream_name: Optional[str] = None,
        stream_arn: Optional[str] = None,
        late_arrival_deadline: Duration = "infinity",
        dead_letter_queue_topic: Optional[str] = None,
        name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        region_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
    ):
        super(KinesisSource, self).__init__(
            stream_name=stream_name,
            stream_arn=stream_arn,
            name=name,
            late_arrival_deadline=late_arrival_deadline,
            dead_letter_queue_topic=dead_letter_queue_topic,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
            endpoint_url=endpoint_url,
        )

    def _config_to_json(self) -> Any:
        return self.json()
