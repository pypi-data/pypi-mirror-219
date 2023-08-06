import io
from dataclasses import dataclass
from typing import List, Dict, Callable, Any, Tuple

import pandas as pd
import requests

from instagrader.config.operations import OperationName
from instagrader.library.commons import print_exception, invoke, serialize
from instagrader.model.Exceptions import ResourceNotFoundException, InstagraderException
from instagrader.model.activity.CreateHomework import CreateHomeworkRequest
from instagrader.model.activity.GetClassGrades import GetClassGradesRequest, GetClassGradesResponse
from instagrader.model.activity.GetHomework import GetHomeworkRequest
from instagrader.model.activity.UpdateHomework import UpdateHomeworkRequest
from instagrader.model.db.Homework import HomeworkConfig


@dataclass
class HomeworkBackend:
    name: str
    account_id: str
    secret_key: str
    deadline: int
    student_ids: List[str]
    max_attempts: int

    def __post_init__(self):
        print('Initializing homework...')
        try:
            self._get_homework()
            self._update_homework_config()
            print('Homework initialized successfully')
        except ResourceNotFoundException as _:
            print(f'Homework named "{self.name}" does not exists, creating new homework...')
            self._create_homework()
        except InstagraderException as exception:
            print_exception(exception)

    def update_test_cases(self, test_cases: Dict[str, Callable[[Any], Tuple]]):
        serialized_test_cases = {test_case_name: serialize(test_case_fun) for (test_case_name, test_case_fun) in test_cases.items()}
        self._update_homework_test_cases(serialized_test_cases)
        print('Test cases updated successfully')

    def get_grades(self) -> pd.DataFrame:
        try:
            response: GetClassGradesResponse = invoke(OperationName.GET_CLASS_GRADES, GetClassGradesRequest(
                account_id=self.account_id,
                secret_key=self.secret_key,
                homework_name=self.name,
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

    def _get_homework(self):
        invoke(OperationName.GET_HOMEWORK, GetHomeworkRequest(
            account_id=self.account_id,
            secret_key=self.secret_key,
            homework_name=self.name
        ))

    def _create_homework(self):
        try:
            invoke(OperationName.CREATE_HOMEWORK, CreateHomeworkRequest(
                account_id=self.account_id,
                secret_key=self.secret_key,
                homework_name=self.name,
                homework_config=HomeworkConfig(
                    deadline=self.deadline,
                    student_emails=list(self.student_ids),
                    max_attempts=self.max_attempts,
                ),
                serialized_test_cases=None
            ))
            print('Homework initialized successfully')
        except InstagraderException as exception:
            print_exception(exception)

    def _update_homework_config(self):
        try:
            invoke(OperationName.UPDATE_HOMEWORK, UpdateHomeworkRequest(
                account_id=self.account_id,
                secret_key=self.secret_key,
                homework_name=self.name,
                homework_config=HomeworkConfig(
                    deadline=self.deadline,
                    max_attempts=self.max_attempts,
                    student_emails=list(self.student_ids)
                ),
                serialized_test_cases=None
            ))
        except InstagraderException as exception:
            print_exception(exception)

    def _update_homework_test_cases(self, serialized_test_cases: Dict[str, str]):
        try:
            invoke(OperationName.UPDATE_HOMEWORK, UpdateHomeworkRequest(
                account_id=self.account_id,
                secret_key=self.secret_key,
                homework_name=self.name,
                homework_config=None,
                serialized_test_cases=serialized_test_cases
            ))
        except InstagraderException as exception:
            print_exception(exception)
