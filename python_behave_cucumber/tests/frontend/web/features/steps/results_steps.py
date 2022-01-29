from behave import step
from hamcrest import assert_that


@step('All the results should match with my search')
def step_impl(context):
    for result in context.page.get_search_results():
        assert_that(context.searched_text.lower() in result.lower(),
                    f"Error while checking results text: \n"
                    f"Actual: [{result.lower()}]\nExpected: [{context.searched_text.lower()}]")


@step('The result in the position "{position}" is opened')
def step_impl(context, position):
    context.page = context.page.open_product('position', int(position))


@step('The result "{result_value}" is opened')
def step_impl(context, result_value):
    context.page = context.page.open_product('value', result_value)


@step('A random result is opened')
def step_impl(context):
    context.page = context.page.open_product()
