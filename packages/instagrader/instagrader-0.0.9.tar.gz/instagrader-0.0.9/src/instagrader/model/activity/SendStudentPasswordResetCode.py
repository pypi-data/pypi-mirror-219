from dataclasses import dataclass

from instagrader.model.activity.Payload import Payload


@dataclass
class SentStudentPasswordResetCodeRequest(Payload):
    student_email: str
