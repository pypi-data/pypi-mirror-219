from dataclasses import dataclass

from instagrader.model.activity.Payload import Payload


@dataclass
class ResetStudentPasswordRequest(Payload):
    student_email: str
    password_reset_code: str
    new_hashed_password: str
