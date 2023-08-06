from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.screen import ModalScreen
from textual.widgets import OptionList, Placeholder, Button

from tuidbtv.config.ConfigParser import ConfigParser
from tuidbtv.controllers.ControllerFactory import ControllerFactory
from tuidbtv.widgets.NewConnection import NewConnection
from tuidbtv.widgets.PopUpScreen import PopUpScreen


class SelectConnection(ModalScreen):
    highlighted_index = 0
    firstRun = True

    def __init__(self, firstRun = False):
        super().__init__()
        self.firstRun = firstRun

    def compose(self) -> ComposeResult:
        yield Grid(
            OptionList(id="select_connection_list"),
            Vertical(
                Button.success("Connect", id="connect_button", disabled=True),
                Button("New Connection", variant="primary", id="new_connection_button"),
                Button("Test connection", id="test_connection_button", disabled=True),
                Button("Edit connection", id="edit_connection_button", disabled=True),
                Button.error("Delete Connection", id="delete_connection_button", disabled=True),
            ),
            Button.warning("Quit" if self.firstRun else "Cancel", id="cancel_select_connection_button"),
            id="select_connection_dialog"
        )

    def on_mount(self):
        optionList: OptionList = self.queryConnectionsList()
        for connection in ConfigParser.readConnectionList():
            optionList.add_option(connection["connectionName"])

    def on_button_pressed(self, event):
        def addNewConnection(connectionName):
            optionList: OptionList = self.queryConnectionsList()
            optionList.add_option(connectionName)

        match event.button.id:
            case "new_connection_button":
                self.parent.push_screen(NewConnection(), addNewConnection)

            case "edit_connection_button":
                selectedConnection: OptionList = self.queryConnectionsList()
                selectedOption = selectedConnection.get_option_at_index(self.highlighted_index).prompt.__str__()
                for connection in ConfigParser.readConnectionList():
                    if connection['connectionName'] == selectedOption:
                        self.parent.push_screen(NewConnection(connection))

            case "connect_button":
                selectedConnection: OptionList = self.queryConnectionsList()
                selectedOption = selectedConnection.get_option_at_index(self.highlighted_index).prompt.__str__()
                for connection in ConfigParser.readConnectionList():
                    if connection['connectionName'] == selectedOption:
                        try:
                            controller = ControllerFactory.getController(connection)
                            self.dismiss(controller)
                        except:
                            self.app.push_screen(PopUpScreen("Some errors happened while trying to connect :c"))
            case "cancel_select_connection_button":
                if self.firstRun:
                    self.app.exit()
                else:
                    self.app.pop_screen()
            case "delete_connection_button":
                selectedConnection: OptionList = self.queryConnectionsList()
                selectedOption = selectedConnection.get_option_at_index(self.highlighted_index).prompt.__str__()
                selectedConnection.remove_option_at_index(self.highlighted_index)
                ConfigParser.removeConnectionByName(selectedOption)
                if selectedConnection.option_count == 0:
                    self.query_one("#connect_button").disabled = True
                    self.query_one("#test_connection_button").disabled = True
                    self.query_one("#edit_connection_button").disabled = True
                    self.query_one("#delete_connection_button").disabled = True

            case "test_connection_button":
                try:
                    selectedConnection: OptionList = self.queryConnectionsList()
                    selectedOption = selectedConnection.get_option_at_index(self.highlighted_index).prompt.__str__()
                    for connection in ConfigParser.readConnectionList():
                        if connection['connectionName'] == selectedOption:
                            # TODO replace with testConnection maybe
                            ControllerFactory.getController(connection)
                            btn: Button = self.query_one("#test_connection_button", expect_type=Button)
                            btn.variant = "success"
                            btn.label = "success"
                except:
                    btn: Button = self.query_one("#test_connection_button", expect_type=Button)
                    btn.variant = "error"
                    btn.label = "error"

    def on_option_list_option_highlighted(self, event: OptionList.OptionMessage):
        self.query_one("#connect_button").disabled = False
        self.query_one("#test_connection_button").disabled = False
        self.query_one("#edit_connection_button").disabled = False
        self.query_one("#delete_connection_button").disabled = False
        self.highlighted_index = event.option_index
        test_connection_button: Button = self.query_one("#test_connection_button", expect_type=Button)
        test_connection_button.variant = "default"
        test_connection_button.label = "Test Connection"

    def queryConnectionsList(self) -> OptionList:
        return self.query_one("#select_connection_list", expect_type=OptionList)

