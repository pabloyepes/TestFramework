from tests.api.api_clients.employees import Employee
from automation_base.config import ApplicationUtils
from env_config import EnvironmentConfig
from utils import Utils


def before_scenario(context, scenario):
    context.current_environment = ApplicationUtils().get_test_environment()
    context.api = Employee(EnvironmentConfig.employees_api()[context.current_environment])


def after_scenario(context, scenario):
    tags = Utils().get_scenario_tags(scenario)
    if hasattr(context, 'created_employees'):
        for employee in context.created_employees:
            context.execute_steps(f'''Then The employee with id "{employee}" is deleted''')
    context.api._response_json_dict = {}
