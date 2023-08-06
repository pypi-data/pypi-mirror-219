from dataclasses import dataclass



@dataclass
class Grade:
    student_score: int
    max_score: int
    message: str
