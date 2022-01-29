from behave import step


@step('The product "{product}" is searched')
def step_impl(context, product):
    context.page = context.page.top_nav_bar.perform_search(product)
    context.searched_text = product
