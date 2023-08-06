from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label, Button


class PopUpScreen(ModalScreen):
    text = ""

    def __init__(self, text):
        super().__init__()
        self.text = text

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.text, id="popup_text"),
            Button("OK", variant="primary", id="popup_ok"),
            id="popup_window",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()
