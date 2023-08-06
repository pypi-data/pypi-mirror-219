from dataclasses import dataclass
from typing import Optional, Dict

from instagrader.model.activity.Payload import Payload
from instagrader.model.db.Homework import HomeworkConfig


@dataclass
class UpdateHomeworkRequest(Payload):
    homework_name: str
    account_id: str
    secret_key: str
    homework_config: Optional[HomeworkConfig]
    serialized_test_cases: Optional[Dict[str, str]]
