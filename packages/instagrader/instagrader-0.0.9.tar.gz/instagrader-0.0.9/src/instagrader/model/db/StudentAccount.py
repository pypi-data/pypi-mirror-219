from dataclasses import dataclass


@dataclass
class StudentAccount:
    email: str              
    hashed_password: str

