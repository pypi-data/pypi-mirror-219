from enum import Enum

from dataclasses import dataclass
from typing import Dict, Type, Optional

from instagrader.model.activity.CreateHomework import CreateHomeworkRequest
from instagrader.model.activity.CreateStudentAccount import CreateStudentAccountRequest
from instagrader.model.activity.GetClassGrades import GetClassGradesRequest, GetClassGradesResponse
from instagrader.model.activity.GetHomework import GetHomeworkRequest, GetHomeworkResponse
from instagrader.model.activity.GetStudentAccount import GetStudentAccountRequest
from instagrader.model.activity.GetStudentGrades import GetStudentGradesRequest, GetStudentGradesResponse
from instagrader.model.activity.GradeSubmission import GradeSubmissionRequest, GradeSubmissionResponse
from instagrader.model.activity.ResetStudentPassword import ResetStudentPasswordRequest
from instagrader.model.activity.SendStudentPasswordResetCode import SentStudentPasswordResetCodeRequest
from instagrader.model.activity.Payload import Payload
from instagrader.model.activity.UpdateHomework import UpdateHomeworkRequest


@dataclass
class Operation:
    request_type: Type[Payload]
    response_type: Optional[Type[Payload]]


class OperationName(Enum):
    CREATE_HOMEWORK = 'CreateHomework'
    GET_HOMEWORK = 'GetHomework'
    UPDATE_HOMEWORK = 'UpdateHomework'
    CREATE_STUDENT_ACCOUNT = 'CreateStudentAccount'
    GET_STUDENT_ACCOUNT = 'GetStudentAccount'
    SEND_STUDENT_PASSWORD_RESET_CODE = 'SendStudentPasswordResetCode'
    RESET_STUDENT_PASSWORD = 'ResetStudentPassword'
    GRADE_SUBMISSION_HANDLER = 'GradeSubmissionHandler'
    GRADE_SUBMISSIONS_HANDLER = 'GradeSubmissionHandler'
    GET_CLASS_GRADES = 'GetClassGrades'
    GET_STUDENT_GRADES = 'GetStudentGrades'


operations: Dict[str, Operation] = {
    OperationName.CREATE_HOMEWORK.value: Operation(
        request_type=CreateHomeworkRequest,
        response_type=None,
    ),
    OperationName.GET_HOMEWORK.value: Operation(
        request_type=GetHomeworkRequest,
        response_type=GetHomeworkResponse,
    ),
    OperationName.UPDATE_HOMEWORK.value: Operation(
        request_type=UpdateHomeworkRequest,
        response_type=None,
    ),
    OperationName.CREATE_STUDENT_ACCOUNT.value: Operation(
        request_type=CreateStudentAccountRequest,
        response_type=None,
    ),
    OperationName.GET_STUDENT_ACCOUNT.value: Operation(
        request_type=GetStudentAccountRequest,
        response_type=None,
    ),
    OperationName.SEND_STUDENT_PASSWORD_RESET_CODE.value: Operation(
        request_type=SentStudentPasswordResetCodeRequest,
        response_type=None,
    ),
    OperationName.RESET_STUDENT_PASSWORD.value: Operation(
        request_type=ResetStudentPasswordRequest,
        response_type=None,
    ),
    OperationName.GRADE_SUBMISSION_HANDLER.value: Operation(
        request_type=GradeSubmissionRequest,
        response_type=GradeSubmissionResponse,
    ),
    OperationName.GET_CLASS_GRADES.value: Operation(
        request_type=GetClassGradesRequest,
        response_type=GetClassGradesResponse,
    ),
    OperationName.GET_STUDENT_GRADES.value: Operation(
        request_type=GetStudentGradesRequest,
        response_type=GetStudentGradesResponse,
    ),
}
