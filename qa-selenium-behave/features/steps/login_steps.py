from behave import given, when, then
from pages.login_page import LoginPage

@given("que estoy en la página de login")
def step_open_login(context):
    context.page = LoginPage(context.driver, context.base_url)
    context.page.open()

@when('inicio sesión con usuario "{user}" y clave "{pwd}"')
def step_do_login(context, user, pwd):
    context.page.login(user, pwd)

@then("debería ver el inventario")
def step_assert_logged_in(context):
    context.page.assert_logged_in()

@then('debería ver un mensaje de error que contiene "{text}"')
def step_assert_error(context, text):
    context.page.assert_error_contains(text)
