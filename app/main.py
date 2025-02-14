import os
from nicegui import ui
import httpx

"""
.classes = tailwind + quasar classes
.props = quasar props
.tailwind()
"""

# TODO Account Creation: Register and login page, link with supabase

API_URL = "https://api.moneymentorapp.tech"
# API_URL = "http://localhost:8080"

# Function to register a new user


async def register(username, password):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_URL}/register", json={"username": username, "password": password})
            if response.status_code == 200:
                ui.notify("Registration successful!", color="positive")
            else:
                ui.notify(f"Error: {response.json()}", color="negative")
    except Exception as e:
        ui.notify(f"An error occurred: {e}", color="negative")

# Function to log in


async def login(username, password):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                token = response.json()["access_token"]
                ui.notify("Login successful!", color="positive")
                # Store the token for future requests
                ui.storage.user.set("token", token)
            else:
                ui.notify(f"Error: {response.json()}", color="negative")
    except Exception as e:
        ui.notify(f"An error occurred: {e}", color="negative")

# Function to update email


async def update_email(email, token):
    if not token:
        ui.notify("You need to log in first!", color="negative")
        return
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_URL}/profile/email", json={"email": email}, headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 200:
                ui.notify("Email updated successfully!", color="positive")
            else:
                ui.notify(f"Error: {response.json()}", color="negative")
    except Exception as e:
        ui.notify(f"An error occurred: {e}", color="negative")


# Function to fetch profile
async def fetch_profile(token):
    if not token:
        ui.notify("You need to log in first!", color="negative")
        return
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/profile", headers={"Authorization": f"Bearer {token}"})
            if response.status_code == 200:
                profile = response.json()["profile"]
                ui.notify(f"Profile: {profile}", color="positive")
            else:
                ui.notify(f"Error: {response.json()}", color="negative")
    except Exception as e:
        ui.notify(f"An error occurred: {e}", color="negative")


class Header:
    def __init__(self):
        self.display()

    def display(self):
        with ui.header().classes("bg-neutral-100"):
            with ui.row().classes("w-full justify-between items-center"):
                with ui.row().classes("items-center"):
                    ui.image("app/logos/logo_green.png") \
                        .classes("w-8 cursor-pointer").on("click", lambda: ui.navigate.reload())
                    ui.label("Welcome, FIRST_NAME LAST_NAME.").classes("text-m font-medium text-neutral-950")
                with ui.row():
                    ui.label("MoneyMentor").classes("font-mono text-xl font-medium text-neutral-950")


class Footer:
    def __init__(self):
        self.display()

    def display(self):

        with ui.footer().classes("border-t-2 border-grey-50 bg-neutral-100"):
            with ui.row().classes("w-full justify-between items-center"):
                with ui.row().classes("items-center gap-2.5 cursor-pointer").on("click", lambda: ui.navigate.reload()):
                    ui.image("app/logos/logo_green.png").classes("w-8")
                    ui.label("MoneyMentor").classes("font-mono text-xl font-medium text-neutral-950")
                with ui.row().classes("gap-0.5"):
                    Footer.footer_label("Visit the ", "neutral-500")
                    Footer.footer_link("MoneyMentor GitHub Repository",
                                       "https://github.com/anthonytoyco/moneymentor", "neutral-500")
                with ui.row().classes("gap-0.5"):
                    Footer.footer_label("Developed by ")
                    Footer.footer_link("Anthony Toyco", "https://github.com/anthonytoyco")
                    Footer.footer_label(", ")
                    Footer.footer_link("Draven Ng", "https://github.com/xDbibix")
                    Footer.footer_label(", & ")
                    Footer.footer_link("Felex Hill", "https://github.com/FelexHill7")

    @staticmethod
    def footer_label(text, text_color="neutral-600"):
        return ui.label(text).classes(f"text-xs font-normal text-{text_color}")

    @staticmethod
    def footer_link(text, link, text_color="neutral-600"):
        return ui.link(text, link).classes(f"text-xs font-normal text-{text_color}")


async def call_api():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()  # Parse JSON response
            ui.notify(f"API Response: {data}")  # Show the response in a notification
    except httpx.HTTPStatusError as e:
        ui.notify(f"HTTP error occurred: {e}", color="negative")
    except Exception as e:
        ui.notify(f"An error occurred: {e}", color="negative")


class Main:
    def __init__(self):
        self.display()

    def display(self):
        ui.query("body").classes("bg-neutral-100")
        with ui.row() as self.main_row:
            with ui.row():
                with ui.card():
                    ui.label("Click the button to call the API")
                    ui.button("Call API", on_click=call_api)
                with ui.card():
                    username_input = ui.input("Username").props("type=text")
                    password_input = ui.input("Password").props("type=password")
                    email_input = ui.input("Email").props("type=email")
                    ui.button("Register", on_click=lambda: register(username_input.value, password_input.value))
                    ui.button("Login", on_click=lambda: login(username_input.value, password_input.value))
                    ui.button("Update Email", on_click=lambda: update_email(
                        email_input.value, ui.storage.user.get("token")))
                    ui.button("Fetch Profile", on_click=lambda: fetch_profile(ui.storage.user.get("token")))


class AnimationExample:
    def __init__(self):
        self.width_class = "w-0"
        self.column = ui.column().classes(f"{self.width_class} transition-all duration-500 bg-blue-100")
        with self.column:
            ui.label("This is a column")
            ui.button("Click me", on_click=lambda: ui.notify("Button clicked!"))
        ui.button("Toggle Column Width", on_click=self.toggle_width)

    def toggle_width(self):
        if self.width_class == "w-0":
            self.width_class = "w-96"
        else:
            self.width_class = "w-0"
        self.column.classes(replace=f"{self.width_class} transition-all duration-500 bg-blue-100")


@ui.page("/")
def index():
    Header(), Footer(), Main()


ui.run(reload="FLY_ALLOC_ID" not in os.environ, title="MoneyMentor", favicon="app/logos/logo_green.png")
