from dataclasses import dataclass

from instagrader.model.activity.Payload import Payload


@dataclass
class GetClassGradesRequest(Payload):
    homework_name: str
    account_id: str
    secret_key: str


@dataclass
class GetClassGradesResponse(Payload):
    output_url: str
