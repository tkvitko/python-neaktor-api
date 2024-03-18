"""
    Official neaktor API documentation:
    https://developers.neaktor.com/#/overview
"""

from typing import Union, List

import requests

from neaktor.constants import DEFAULT_PAGE_SIZE


class NoAuthParam(Exception):
    pass


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
                          ) -> dict:
        """
        Base request to neaktor web api
        :param api_path: api path
        :param body: request body
        :param method: HTTP method
        :return:
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
        if response is not None:
            return response.json()

    def _get_objects(self,
                     api_path: str,
                     params: dict = None,
                     page_size: int = DEFAULT_PAGE_SIZE,
                     ) -> Union[List[dict], None]:
        """
        Base request for any neaktor objects list
        :param api_path: api path
        :param params: any get parameters
        :param page_size: objects number per page
        :return: objects list
        """

        api_path += f'?size={page_size}'
        if params is not None:
            api_path += '&'
            params_list = [f'{field}={value}' for field, value in params.items()]
            api_path += '&'.join(params_list)

        data = list()
        page_number = 0
        total = page_size + 1

        while len(data) < total:
            current_api_path = api_path + f'&page={page_number}'
            print(current_api_path)
            result = self._base_api_request(api_path=current_api_path, method='GET')
            data += result['data']
            total = result['total']
            page_number += 1

        return data

    def _add_object(self,
                    api_path: str,
                    parent_id: str,
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
        body = dict()

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

        return result

    def get_tasks(self,
                  page_size: int = DEFAULT_PAGE_SIZE,
                  **params
                  ) -> List[dict]:
        """
        https://developers.neaktor.com/#/tasks
        :param page_size: objects number per page
        :param params: any get parameters
        :return: tasks list
        """

        api_path = 'v1/tasks'
        objects = self._get_objects(api_path=api_path,
                                    page_size=page_size,
                                    params=params)
        return objects

    def get_task_modes(self,
                       page_size: int = DEFAULT_PAGE_SIZE,
                       **params
                       ) -> List[dict]:
        """
        https://developers.neaktor.com/#/taskmodels
        :param page_size: objects number per page
        :param params: any get parameters
        :return: tasks list
        """

        api_path = 'v1/taskmodels'
        objects = self._get_objects(api_path=api_path,
                                    page_size=page_size,
                                    params=params)
        return objects

    def get_users(self,
                  page_size: int = DEFAULT_PAGE_SIZE,
                  **params
                  ) -> List[dict]:
        """
        https://developers.neaktor.com/#/users
        :param page_size: objects number per page
        :param params: any get parameters
        :return: users list
        """

        api_path = 'v1/users'
        objects = self._get_objects(api_path=api_path,
                                    page_size=page_size,
                                    params=params)
        return objects

    def add_task(self,
                 model_id: str,
                 fields: dict = None,
                 assignee_id: int = None,
                 assignee_type: str = 'USER'
                 ) -> Union[dict | None]:
        """
        https://developers.neaktor.com/#/tasks/id/create
        :param model_id: id of model to create task to
        :param fields: dict of task fields
        :param assignee_id: id of assignee
        :param assignee_type: type of assignee ('USER', 'GROUP')
        :return: created task
        """

        result = self._add_object(api_path='v1/tasks',
                                  parent_id=model_id,
                                  fields=fields,
                                  assignee_id=assignee_id,
                                  assignee_type=assignee_type)

        return result

    def add_comment(self,
                    task_id: str,
                    text: str
                    ) -> Union[dict | None]:
        """
        https://developers.neaktor.com/#/comments/create
        :param task_id: if of task to add comment to
        :param text: text to add comment with
        :return:
        """

        result = self._add_object(api_path='v1/comments',
                                  parent_id=task_id,
                                  text=text)

        return result
