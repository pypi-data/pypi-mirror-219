# coding=utf-8
"""
作者：vissy@zhu
"""

import requests
import urllib3
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class ConfigHttp():

    def __init__(self, scheme, api_url, www_url, web_url, port):
        self.scheme = scheme
        self.api_url = api_url
        self.www_url = www_url
        self.web_url = web_url
        self.port = port
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = {}
        # self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.__url = self.scheme + '://' + self.api_url + url

    def set_www_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.__url = self.scheme + '://' + self.www_url + url

    def set_web_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.__url = self.scheme + '://' + self.web_url + url

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.__data = data

    # defined http_data.py get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            urllib3.disable_warnings()
            response = requests.get(self.__url, headers=self.headers, params=self.params, verify=False)
            # response.raise_for_status()
            return response
        except TimeoutError:
            return None

    # defined http_data.py post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            urllib3.disable_warnings()
            response = requests.post(self.__url, headers=self.headers, json=self.__data, verify=False)
            # response.raise_for_status()
            return response
        except TimeoutError:
            return None

    def delete(self):
        """
        defined delete method
        :return:
        """
        try:
            urllib3.disable_warnings()
            response = requests.delete(self.__url, headers=self.headers, params=self.data, verify=False)
            return response
        except TimeoutError:
            return None

    def put(self):
        """
        defined post method
        :return:
        """
        try:
            urllib3.disable_warnings()
            response = requests.put(self.__url, headers=self.headers, json=self.__data, verify=False)
            return response
        except TimeoutError:
            return None
