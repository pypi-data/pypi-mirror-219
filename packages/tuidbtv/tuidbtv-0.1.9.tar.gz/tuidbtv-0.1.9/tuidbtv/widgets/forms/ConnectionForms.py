from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input

from tuidbtv.controllers.MySQLController import MySQLController
from tuidbtv.controllers.PostgresController import PostgresController
from tuidbtv.controllers.SQLLiteController import SQLLiteController


class ConnectionForms(Widget):
    DEFAULT_CSS = """
        ConnectionForms{ column-span: 3; }
    """

    def __init__(self, connectionType: str):
        super().__init__()
        self.form = None
        self.connectionType = connectionType
        self.selectForm(connectionType)

    def compose(self) -> ComposeResult:
        yield self.form()

    def prepopulateData(self, data_to_edit: dict) -> None:
        if data_to_edit is not None:
            for field_key in data_to_edit.keys():
                if field_key not in ["connectionType", "connectionName"]:
                    field = self.query_one(f"#{field_key}", expect_type=Input)
                    field.value = data_to_edit[field_key]

    def selectForm(self, connectionType: str):
        self.connectionType = connectionType
        # TODO move to Controller_factory
        match connectionType:
            case "postgresql":
                self.form = PostgresController.get_connection_form
            case "mysql":
                self.form = MySQLController.get_connection_form
            case _:
                self.form = SQLLiteController.get_connection_form

    def changeForm(self, connectionType: str):
        fields = self.query_one('#connection_form')
        fields.remove()
        self.selectForm(connectionType)
        self.mount(self.form())
