from dataclasses import dataclass

from instagrader.model.activity.Payload import Payload


@dataclass
class CreateStudentAccountRequest(Payload):
    email: str
    hashed_password: str
