from dataclasses import dataclass

from instagrader.model.activity.Payload import Payload
from instagrader.model.db.Homework import Homework


@dataclass
class GetHomeworkRequest(Payload):
    homework_name: str
    account_id: str
    secret_key: str


@dataclass
class GetHomeworkResponse(Payload):
    homework: Homework

