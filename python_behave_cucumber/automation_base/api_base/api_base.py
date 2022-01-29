import ast
import json
import logging
import urllib.parse

from requests.sessions import session

from automation_base.singleton import Singleton


class BaseAPI(object, metaclass=Singleton):

    def __init__(self, base_url):
        self.base_url = base_url
        self.req = session()
        self.response = None
        self.default_headers = {'Content-Type': 'application/json'}
        self.query_params = {}
        self._response_json_dict = {}

    @property
    def response_json_dict(self):
        if self.response is not None and self.response.content:
            self._response_json_dict = self.get_json(self.response)
        else:
            self._response_json_dict = {}
        return self._response_json_dict

    @staticmethod
    def get_json(response):
        """
        Given a HTTP query response, returns it JSON content.
        :param response:  Dict    HTTP query response.
        :return:          Dict    JSON response content.
        """
        return response.json()

    def add_query_parameter(self, key, value):
        """
        Adds a new query parameter to be appended in the query rest url.
        :param key:     String      Query parameter key.
        :param value:   String      Query parameter value.
        """
        self.query_params[key] = value

    def clear_query_parameters(self):
        """
        Clears the query parameter list.
        """
        self.query_params = {}

    @staticmethod
    def add_url_query_parameters(url, query_params):
        """
        Adds query parameters to a URL

        :param url: A string representing the URL to add the parameters to
        :param query_params: A JSON dict representing the query parameters as key: value
        :return: A string representing the new URL with the added query parameters
        """
        (scheme, netloc, path, params, query, fragment) = urllib.parse.urlparse(url)
        url_query_params = urllib.parse.parse_qsl(query, keep_blank_values=True)

        for key in query_params:
            url_query_params.append((key, query_params[key]))

        return urllib.parse.urlunparse((scheme, netloc, path, params,
                                        urllib.parse.urlencode(url_query_params), fragment))

    def execute_service(self, rest_url, operation_type, headers=None, data=None, url_encode=False,
                        data_format='json', log_response=True, **optional):
        """
        Sends a REST request of any kind.
        :param rest_url:          A string representing the resource's URL.
        :param operation_type:    HTTP method.
        :param headers:           (optional) A JSON representation of the headers.
        :param data:              (optional) A JSON representation of the payload.
        :param url_encode:         (optional) URL encode.
        :param log_response:      (optional) False if the response text should not be logged.
        :param data_format:
            (optional) Converts the data into appropriate objects. Default value 'json' encode it to a JSON object.
        :returns:                 The response object.
        """
        if headers is None:
            headers = self.get_default_headers()
        if data is None:
            data = {}

        headers_log = {value: '***' for value in headers.copy()}
        logging.info(f'Headers: {headers_log}')

        if len(data) > 0:
            logging.info(f'Payload: {data}')

        if url_encode:
            data = urllib.parse.urlencode(data)
        else:
            if data_format.lower() == 'json':
                data = json.dumps(data)

        url = self.base_url + rest_url

        if len(self.query_params) > 0:
            url = self.add_url_query_parameters(url, self.query_params)

        logging.info(f'Sending {operation_type} request to {url}')

        if operation_type == "POST":
            self.response = self.req.post(url, headers=headers, data=data, **optional)
        elif operation_type == "GET":
            self.response = self.req.get(url, headers=headers, **optional)
        elif operation_type == "HEAD":
            self.response = self.req.head(url, headers=headers, **optional)
        elif operation_type == "OPTIONS":
            self.response = self.req.options(url, headers=headers, data=data, **optional)
        elif operation_type == "PUT":
            self.response = self.req.put(url, headers=headers, data=data, **optional)
        elif operation_type == "PATCH":
            self.response = self.req.patch(url, headers=headers, data=data, **optional)
        elif operation_type == "DELETE":
            self.response = self.req.delete(url, headers=headers, data=data, **optional)

        logging.info(f'REST operation finished with status code {str(self.response.status_code)}: '
                     f'{self.response.reason}')

        if log_response:
            logging.info(f'Service response: {self.response.text}')

        self.clear_query_parameters()

        return self.response

    def get_response_header(self, header):
        return str(self.response.headers[header.title()])

    def set_default_headers(self, headers):
        """
        Sets defaults headers to API service.
        :param headers:   Dict    New default headers.
        :return:          None
        """
        if isinstance(headers, str):
            self.default_headers = ast.literal_eval(headers)
        else:
            self.default_headers = headers

    def get_default_headers(self):
        """
        Gets defaults headers from API service.
        :return:      Dict    Default headers.
        """
        return self.default_headers
