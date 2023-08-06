from dataclasses import dataclass
from typing import List, Dict


@dataclass
class HomeworkConfig:
    deadline: int
    student_emails: List[str]
    max_attempts: int


@dataclass
class Homework:
    name: str  # [PartitionKey]
    account_id: str
    config: HomeworkConfig
    serialized_test_cases: Dict[str, str]
