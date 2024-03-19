"""
    Official neaktor API documentation:
    https://developers.neaktor.com/#/overview
"""

from typing import Union, List

import requests

from .constants import DEFAULT_PAGE_SIZE
from .exceptions import NoAuthParam, NeaktorException
from .objects import User, Task, TaskModel, Comment


class NeaktorApiClient:
    """
    Main class of API wrapper
    """

    def __init__(self,
                 public_key: str = None,
                 access_token: str = None,
                 timeout: int = 60):

        # base params:
        self.base_url = 'https://api.neaktor.com/'
        self.timeout = timeout

        # authorization params:
        if (public_key, access_token).count(None) == 2:
            raise NoAuthParam()
        if public_key is not None:
            self.public_key = public_key
            self.request_headers = {'Authorization': self.public_key}
        if access_token is not None:
            self.access_token = access_token
            self.request_headers = {'Authorization': 'Bearer: ' + self.access_token}

    def _base_api_request(self, api_path: str,
                          body: Union[dict, list] = None,
                          method: str = 'GET'
                          ) -> Union[dict, List[dict], None]:
        """
        Base request to neaktor web api
        :param api_path: api path
        :param body: request body
        :param method: HTTP method
        :return: dict of response bods
        """

        response = None
        if method == 'GET':
            response = requests.get(url=self.base_url + api_path,
                                    headers=self.request_headers,
                                    timeout=self.timeout)

        elif method == 'POST':
            response = requests.post(url=self.base_url + api_path,
                                     headers=self.request_headers,
                                     timeout=self.timeout,
                                     json=body)

        elif method == 'DELETE':
            response = requests.delete(url=self.base_url + api_path,
                                       headers=self.request_headers,
                                       timeout=self.timeout,
                                       json=body)

        if response is not None:
            return response.json()
        return None

    def _get_objects(self,
                     api_path: str,
                     params: dict = None,
                     page_size: int = DEFAULT_PAGE_SIZE,
                     object_ids: set = None,
                     ) -> Union[List[dict], None]:
        """
        Base request for any neaktor objects list
        :param api_path: api path
        :param params: any get parameters
        :param page_size: objects number per page
        :param object_ids: set of certain objects to get
        :return: objects list
        """

        if object_ids:
            object_ids = map(str, object_ids)
            api_path += ",".join(object_ids)
            result = self._base_api_request(api_path=api_path, method='GET')
            return result

        api_path += f'?size={page_size}'
        if len(params) > 0:
            api_path += '&'
            params_list = [f'{field}={value}' for field, value in params.items()]
            api_path += '&'.join(params_list)

        data = []
        page_number = 0
        total = page_size + 1

        while len(data) < total:
            current_api_path = api_path + f'&page={page_number}'
            result = self._base_api_request(api_path=current_api_path, method='GET')
            data += result['data']
            total = result['total']
            page_number += 1

        return data

    def _add_object(self,
                    api_path: str,
                    parent_id: Union[int, str],
                    fields: dict = None,
                    assignee_id: int = None,
                    assignee_type: str = 'USER',
                    text: str = None,
                    ) -> Union[dict, None]:
        """
        Base request for any neaktor object create
        :param api_path: api path
        :param parent_id: id of the parent entity
        :param fields: list of entity fields
        :param assignee_id: id of assignee
        :param assignee_type: type of assignee ('USER', 'GROUP')
        :param text: text for comment
        :return: created object
        """

        api_path += f'/{parent_id}'
        body = {}

        if assignee_id is not None:
            body['assignee'] = {'id': assignee_id,
                                'type': assignee_type}

        if text is not None:
            body['text'] = text

        if fields is not None:
            body['fields'] = [{
                'id': field[0],
                'value': field[1],
                'state': 'editable'} for field in fields.items()]

        result = self._base_api_request(api_path=api_path,
                                        body=body,
                                        method='POST')

        if 'id' in result:
            return result
        raise NeaktorException(answer=result)

    def _delete_object(self,
                       api_path: str,
                       object_id: int = None,
                       object_ids: set[int] = None,
                       ) -> Union[dict, None]:
        """
        Base request for any neaktor object delete
        :param api_path: api path
        :param object_id: id of the object
        :return: result of deletion
        """

        body = list(object_ids) if object_ids is not None else None
        api_path = api_path + f'/{object_id}' if object_id is not None else api_path
        result = self._base_api_request(api_path=api_path, method='DELETE', body=body)

        if 'deleted' in result:
            if result['deleted'] is True:
                return result
        raise NeaktorException(answer=result)

    def get_tasks(self,
                  page_size: int = DEFAULT_PAGE_SIZE,
                  task_ids: set = None,
                  **params
                  ) -> List[Task]:
        """
        https://developers.neaktor.com/#/tasks
        :param task_ids: set of task ids to get
        :param page_size: objects number per page
        :param params: any get parameters
        :return: list of Tasks objects
        """

        api_path = 'v1/tasks/'
        task_objs = self._get_objects(api_path=api_path,
                                      page_size=page_size,
                                      object_ids=task_ids,
                                      params=params)

        tasks = [Task(data=task_obj) for task_obj in task_objs]
        return tasks

    def get_task_models(self,
                        page_size: int = DEFAULT_PAGE_SIZE,
                        task_ids: set = None,
                        **params
                        ) -> List[TaskModel]:
        """
        https://developers.neaktor.com/#/taskmodels
        :param task_ids: set of task models ids to get
        :param page_size: objects number per page
        :param params: any get parameters
        :return: list of TaskModels objects
        """

        api_path = 'v1/taskmodels/'
        task_model_objs = self._get_objects(api_path=api_path,
                                            page_size=page_size,
                                            object_ids=task_ids,
                                            params=params)
        task_models = [TaskModel(data=task_model_obj) for task_model_obj in task_model_objs]
        return task_models

    def get_users(self,
                  page_size: int = DEFAULT_PAGE_SIZE,
                  user_ids: set = None,
                  **params
                  ) -> List[User]:
        """
        https://developers.neaktor.com/#/users
        :param user_ids: set of user ids to get
        :param page_size: objects number per page
        :param params: any get parameters
        :return: list of User objects
        """

        api_path = 'v1/users/'
        user_objs = self._get_objects(api_path=api_path,
                                      page_size=page_size,
                                      object_ids=user_ids,
                                      params=params)

        users = [User(data=user_obj) for user_obj in user_objs]
        return users

    def add_task(self,
                 model_id: str,
                 fields: dict = None,
                 assignee_id: int = None,
                 assignee_type: str = 'USER'
                 ) -> Union[Task | None]:
        """
        https://developers.neaktor.com/#/tasks/id/create
        :param model_id: id of model to create task to
        :param fields: dict of task fields
        :param assignee_id: id of assignee
        :param assignee_type: type of assignee ('USER', 'GROUP')
        :return: created Task object
        """

        new_task_obj = self._add_object(api_path='v1/tasks',
                                        parent_id=model_id,
                                        fields=fields,
                                        assignee_id=assignee_id,
                                        assignee_type=assignee_type)

        new_task = Task(data=new_task_obj)
        return new_task

    def delete_task(self,
                    task_id: int
                    ) -> dict:
        """
        https://developers.neaktor.com/#/tasks/id/delete
        :param task_id: id of task
        :return: result of deletion
        """
        result = self._delete_object(api_path='v1/tasks',
                                     object_id=task_id)
        return result

    def add_comment(self,
                    task_id: str,
                    text: str
                    ) -> Union[Comment | None]:
        """
        https://developers.neaktor.com/#/comments/create
        :param task_id: if of task to add comment to
        :param text: text to add comment with
        :return: created Comment object
        """

        new_comment_obj = self._add_object(api_path='v1/comments',
                                           parent_id=task_id,
                                           text=text)

        new_comment = Comment(data=new_comment_obj)
        return new_comment
