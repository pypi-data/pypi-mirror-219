from dataclasses import dataclass
from typing import Dict, Optional

from instagrader.model.activity.Payload import Payload
from instagrader.model.db.Homework import HomeworkConfig


@dataclass
class CreateHomeworkRequest(Payload):
    homework_name: str
    account_id: str
    secret_key: str
    homework_config: HomeworkConfig
    serialized_test_cases: Optional[Dict[str, str]]
