import io
from typing import Any

from getpass import getpass

import pandas as pd
import requests

from instagrader.config.operations import OperationName
from instagrader.library.commons import print_exception, invoke, serialize
from instagrader.model.Exceptions import ResourceNotFoundException, AccessDeniedException, MaxAttemptsReachedException, \
    InstagraderException
from instagrader.model.activity.CreateStudentAccount import CreateStudentAccountRequest
from instagrader.model.activity.GetStudentAccount import GetStudentAccountRequest
from instagrader.model.activity.GetStudentGrades import GetStudentGradesResponse, GetStudentGradesRequest
from instagrader.model.activity.GradeSubmission import GradeSubmissionRequest, GradeSubmissionResponse


class Grader:
    student_id: str
    password: str
    homework_name: str

    def __init__(self, student_id: str, pin: str, homework_name: str):
        try:
            self._get_student(student_id, pin)
        except ResourceNotFoundException as _:
            print(f'Student with ID "{student_id}" does not exists\nCreating new student account...')
            self._create_student(student_id, pin)
            print("Student account created successfully")
        except AccessDeniedException as _:
            print("Email / Pin combination is invalid. Ask your TA to reset your pin!")
            return
        self.student_email = student_id
        self.password = pin
        self.homework_name = homework_name
        print('Grader initialized successfully!')

    def grade(self, test_case_name: str, answer: Any):
        try:
            response: GradeSubmissionResponse = invoke(OperationName.GRADE_SUBMISSION_HANDLER, GradeSubmissionRequest(
                student_email=self.student_email,
                student_hashed_password=self.password,
                homework_name=self.homework_name,
                test_case_name=test_case_name,
                serialized_answer=serialize(answer)
            ))
        except MaxAttemptsReachedException as exception:
            print(f"[ERROR] {exception}. We will use your latest submitted answer.")
            return
        print(f"Submission score: {response.grade.student_score}/{response.grade.max_score}")
        if response.grade.student_score != response.grade.max_score:
            print(f"Attempts remaining: {response.attempts_remaining}")

    def get_homework_grade(self):
        try:
            response: GetStudentGradesResponse = invoke(OperationName.GET_STUDENT_GRADES, GetStudentGradesRequest(
                homework_name=self.homework_name,
                student_email=self.student_email,
                student_hashed_password=self.password
            ))
            data_response = requests.get(response.output_url)
            if data_response.ok:
                data = data_response.content.decode('utf8')
                if len(data) > 1:
                    return pd.read_csv(io.StringIO(data), sep='\t')
                else:
                    print('No student submissions found')
        except InstagraderException as exception:
            print_exception(exception)
    def _get_student(self, student_id: str, password: str):
        invoke(OperationName.GET_STUDENT_ACCOUNT, GetStudentAccountRequest(
            email=student_id,
            hashed_password=password
        ))

    def _create_student(self, student_id, password: str):
        invoke(OperationName.CREATE_STUDENT_ACCOUNT, CreateStudentAccountRequest(
            email=student_id,
            hashed_password=password
        ))