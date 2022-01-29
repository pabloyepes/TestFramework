from behave import step
from hamcrest import assert_that


@step('The product image should load')
def my_step(context):
    assert_that(context.page.driver_base.is_element_displayed('product_image'),
                "The image for the given product did not loaded")
