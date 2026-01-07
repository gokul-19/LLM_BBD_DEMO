from behave import given, when, then

# For a real app, replace this in‑memory state with Playwright / Selenium page objects.
class FakeWebApp:
    def __init__(self):
        self._users = {"alice@example.com": "password123"}
        self.current_page = "login"
        self.error = None

    def login(self, username: str, password: str):
        if self._users.get(username) == password:
            self.current_page = "dashboard"
            self.error = None
        else:
            self.current_page = "login"
            self.error = "Invalid credentials"

app = FakeWebApp()

@given("a registered user exists with email 'alice@example.com' and password 'password123'")
def step_impl_user_exists(context):
    # Already seeded in FakeWebApp
    context.app = app

@given("the user is on the login page")
def step_impl_on_login(context):
    context.app.current_page = "login"

@when("the user submits valid credentials")
def step_impl_submit_valid(context):
    context.app.login("alice@example.com", "password123")

@when("the user submits invalid credentials")
def step_impl_submit_invalid(context):
    context.app.login("alice@example.com", "wrong")

@then("the user should be redirected to the dashboard")
def step_impl_on_dashboard(context):
    assert context.app.current_page == "dashboard"

@then("an error message should be displayed and the user should stay on the login page")
def step_impl_error(context):
    assert context.app.current_page == "login"
    assert context.app.error is not None
