import os
from nicegui import ui
from quotes import Quotes

quotes = Quotes()
ui.button("Quote", on_click=lambda: ui.notify(quotes.random()[1]))

ui.label("Test Label")
ui.label("Test Label")

ui.run(reload="FLY_ALLOC_ID" not in os.environ)
