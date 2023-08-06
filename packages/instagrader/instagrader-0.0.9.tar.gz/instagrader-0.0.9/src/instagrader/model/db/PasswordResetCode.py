from dataclasses import dataclass


@dataclass
class PasswordResetCode:
    student_email: str             
    code: str
    expiration_epoch: int
