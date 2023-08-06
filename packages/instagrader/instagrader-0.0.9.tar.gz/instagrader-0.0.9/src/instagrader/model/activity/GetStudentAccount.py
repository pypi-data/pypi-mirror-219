from dataclasses import dataclass

from instagrader.model.activity.Payload import Payload


@dataclass
class GetStudentAccountRequest(Payload):
    email: str
    hashed_password: str


@dataclass
class GetStudentAccountResponse(Payload):
    email: str
