from behave import step
from hamcrest import assert_that, equal_to, greater_than, is_not

from utils import Utils


def check_employee(employee):
    assert_that(employee.get('id') is not None)
    assert_that(employee.get('employee_name', ''), is_not(equal_to('')))
    assert_that(employee.get('employee_salary', ''), is_not(equal_to('')))
    assert_that(employee.get('employee_age', ''), is_not(equal_to('')))
    assert_that(employee.get('profile_image'), is_not(equal_to(None)))
    return True


@step('All the employees should be properly listed')
def step_impl(context):
    context.api.load_employees()
    assert_that(context.api.response.status_code, equal_to(200),
                'Error while validating load employee list status code')
    assert_that(len(context.api.response_json_dict), greater_than(0),
                'The load employees endpoint did not returned any employee')
    assert_that(all(check_employee(employee) for employee in context.api.response_json_dict))


@step('The employee with id "{employee_id}" is loaded')
def step_impl(context, employee_id):
    context.api.load_employee(employee_id)
    assert_that(context.api.response.status_code, equal_to(200),
                'Error while validating load employee status code')
    assert_that(context.api.response_json_dict[0]['id'], equal_to(int(employee_id)))
    assert_that(check_employee(context.api.response_json_dict[0]))


@step('The following employees are updated')
def step_impl(context):
    for row in context.table.rows:
        formatted_data = Utils().row_to_dict(row)
        context.api.update_employee(formatted_data)
        assert_that(context.api.response.status_code, equal_to(200))


@step('The employees with the following data are created')
def step_impl(context):
    if not hasattr(context, 'created_employees'):
        context.created_employees = []
    for row in context.table.rows:
        formatted_data = Utils().row_to_dict(row)
        context.api.create_employee(formatted_data)
        assert_that(context.api.response.status_code, equal_to(201))
        context.created_employees.append(context.api.response_json_dict['id'])


@step('The created employees are validated')
def step_impl(context):
    for employee_id in context.created_employees:
        context.execute_steps(f'''Then The employee with id "{employee_id}" is loaded''')


@step('The employee with id "{employee_id}" is deleted')
def step_impl(context, employee_id):
    context.api.delete_employee(employee_id)
    assert_that(context.api.response.status_code in [200, 404])
