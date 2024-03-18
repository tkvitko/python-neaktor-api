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
                 public_key:    str = None,
                 access_token:  str = None,
                 timeout:       int = 60):

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

        if method == 'GET':
            response = requests.get(url=self.base_url + api_path,
                                    headers=self.request_headers,
                                    timeout=self.timeout)
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

    def get_tasks(self,
                  page_size: int = DEFAULT_PAGE_SIZE,
                  **params):
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

    def get_users(self,
                  page_size: int = DEFAULT_PAGE_SIZE,
                  **params):
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
