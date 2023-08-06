from dataclasses import dataclass


@dataclass
class TeacherAccount:
    account_id: str  
    secret_key: str
    email: str
    active: bool