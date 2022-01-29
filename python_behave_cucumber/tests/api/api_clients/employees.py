import requests

from automation_base.api_base.api_base import BaseAPI
from automation_base.config import ApplicationUtils


class Employee(BaseAPI):
    def __init__(self, base_url):
        super(Employee, self).__init__(base_url)
        self.req = requests.Session()
        self.access_token = None
        self._account = None

    def set_access_token(self, response_body):
        self.access_token = response_body['access']

    @property
    def auth_header(self):
        return {"Authorization": "Bearer {}".format(self.access_token)}

    def login(self, user):
        """
        Logs in - Not doing anything as the endpoint doesn't needs to login (just for demo purpose)
        :param user:        String  User that is going to login
        :return: Returns the response of the login with valid credentials.
        """
        url = f"/login"
        headers = {"Content-Type": "application/json",
                   "x-api-key": ApplicationUtils().get_login_token()
                   }
        payload = {"email": ApplicationUtils().get_user_email(user),
                   "password": ApplicationUtils().get_user_password(user),
                   }

          # self.execute_service(url, 'POST', headers, payload)
        self.set_access_token({"access": '1234456'})

    def load_employees(self):
        url = f"/employees"
        self.response = self.execute_service(url, 'GET')

    def load_employee(self, employee_id):
        url = f"/employee/{employee_id}"
        self.response = self.execute_service(url, 'GET')

    def create_employee(self, employee):
        url = f"/employees"
        self.response = self.execute_service(url, 'POST', data=employee)
        return self.response_json_dict

    def update_employee(self, new_data):
        url = f"/employees/{new_data['id']}"
        self.response = self.execute_service(url, 'PUT', data=new_data)
        return self.response_json_dict

    def delete_employee(self, employee_id):
        url = f"/employees/{employee_id}/"
        self.response = self.execute_service(url, 'DELETE', headers=None)
        return self.response_json_dict
