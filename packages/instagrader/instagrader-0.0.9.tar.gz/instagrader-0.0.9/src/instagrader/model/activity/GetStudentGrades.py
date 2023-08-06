from dataclasses import dataclass

from instagrader.model.activity.Payload import Payload


@dataclass
class GetStudentGradesRequest(Payload):
    homework_name: str
    student_email: str
    student_hashed_password: str


@dataclass
class GetStudentGradesResponse(Payload):
    output_url: str
