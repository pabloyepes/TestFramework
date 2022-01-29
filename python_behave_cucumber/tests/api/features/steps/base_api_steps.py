from behave import step


@step('The "{user}" user is logged in')
def step_impl(context, user):
    context.api.login(user)
