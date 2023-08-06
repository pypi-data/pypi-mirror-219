from textual import on
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable, Tree

from tuidbtv.signals import PreviewNeed
from tuidbtv.widgets.PopUpScreen import PopUpScreen


class PreviewData(Widget):

    def __init__(self):
        super().__init__()
        self.selected_table = None
        self.selected_schema = None
        self.order_column = None
        self.desc = None

    def compose(self) -> ComposeResult:
        yield DataTable(id="preview_data_table")

    @on(Tree.NodeSelected)
    def refresh_table_data(self, event: Tree.NodeSelected):
        if not event.node.allow_expand:
            self.selected_schema = event.node.parent.label
            self.selected_table = event.node.label
            self.order_column = None
            self.desc = None
            self.post_message(PreviewNeed(self.selected_schema,
                                          self.selected_table,
                                          None,
                                          None))

    @on(DataTable.HeaderSelected)
    def _refresh_sorted_table_data(self, event: DataTable.HeaderSelected):
        column_name = event.label.__str__()
        if self.order_column == column_name:
            self.desc = not self.desc
        else:
            self.order_column = column_name
        self.post_message(PreviewNeed(self.selected_schema,
                                      self.selected_table,
                                      self.order_column,
                                      self.desc))

    def populate_data(self, data):
        table = self.query_one("#preview_data_table")
        table.clear(columns=True)
        table.add_columns(*data[0])
        table.zebra_stripes = True
        table.add_rows(data[1:])
