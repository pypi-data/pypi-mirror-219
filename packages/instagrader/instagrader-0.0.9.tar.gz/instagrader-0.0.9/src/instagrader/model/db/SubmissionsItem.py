from dataclasses import dataclass


@dataclass
class SubmissionsItem:
    student_email: str
    test_case_name: str
    submissions_count: int
