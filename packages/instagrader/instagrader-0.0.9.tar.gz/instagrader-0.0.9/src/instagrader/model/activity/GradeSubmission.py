from dataclasses import dataclass

from instagrader.model.activity.Payload import Payload
from instagrader.model.db.GradeBookItem import Grade


@dataclass
class GradeSubmissionRequest(Payload):
    student_email: str
    student_hashed_password: str
    homework_name: str
    test_case_name: str
    serialized_answer: str


@dataclass
class GradeSubmissionResponse(Payload):
    grade: Grade
    attempts_remaining: int
