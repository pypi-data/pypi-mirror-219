import json
import base64
import dill
import requests
import time
import logging
from dataclasses import asdict
from typing import Dict, Any, Type

from typing import Optional, Type, Any
from instagrader.model.Exceptions import InvalidInputException
from instagrader.config.operations import OperationName, operations
from instagrader.model.Exceptions import InstagraderException, raise_exception, InternalServerException
from instagrader.model.activity.Payload import Payload
from dacite import from_dict, Config


def print_exception(exception: InstagraderException):
    print(f'\n[ERROR] {exception.error_message}')


def invoke(operation: OperationName, data: Payload):
    api_url: str = 'https://hhf9auel47.execute-api.us-east-1.amazonaws.com/default'
    endpoint: str = f'{api_url}/{operation.value}'
    response = requests.post(endpoint, data=json.dumps(dataclass_to_dict(data)))
    if response.status_code == 200:
        operation_response_type: Optional[Type[Payload]] = operations[operation.value].response_type
        return None if operation_response_type is None else dict_to_dataclass(operation_response_type, response.json())
    if 'exceptionName' in response.json() and 'errorMessage' in response.json():
        raise_exception(response.json()['exceptionName'], response.json()['errorMessage'])
    else:
        request_id: str = response.headers['x-amzn-RequestId'] if 'x-amzn-RequestId' in response.headers else response.headers
        error_message: str = f'Uh oh, something went wrong really wrong. If this error persists please contact hello@instagrader.io and provide us this request ID: {request_id}'
        raise InternalServerException(error_message)


def serialize(obj: Any) -> str:
    try:
        byte_serialized = dill.dumps(obj, recurse=True)
        return base64.b64encode(byte_serialized).decode("utf-8")
    except Exception as exception:
        logger.error(f'Failed to serialize object "{obj}" with exception: {exception}')
        raise InvalidInputException(f'Failed to encode input with exception: {exception}')


def deserialize(obj: str) -> Any:
    try:
        byte_decoded = base64.b64decode(obj)
        return dill.loads(byte_decoded)
    except Exception as exception:
        logger.error(f'Failed to parse object "{obj}" with exception: {exception}')
        raise InvalidInputException(f'Failed to parse input with exception: {exception}')



def get_current_utc_epoch() -> int:
    return int(time.time())



def parse_event(data_class: Type[Payload], event: Dict[str, Any]) -> Type[Payload]:
    data: Dict[str, Any] = json.loads(base64_decode(event['body']))
    instance: data_class = dict_to_dataclass(data_class, data)
    return instance



def dict_to_dataclass(data_class: Any, data: Dict) -> Any:  # TODO: Change type
    return from_dict(data_class=data_class, data=data, config=Config(
        type_hooks={
            bool: bool,
            str: str,
            int: int,
            float: float
        }
    ))



def dataclass_to_dict(instance: Any) -> Dict[Any, Any]:
    return asdict(instance)


def base64_decode(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string


