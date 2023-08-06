from textual.message import Message


class PreviewNeed(Message, bubble=True):
    def __init__(self,
                 schema_name: str,
                 table_name: str,
                 column_name: str | None,
                 desc: bool | None):
        self.schema = schema_name
        self.table = table_name
        self.column = column_name
        self.desc = desc
        super().__init__()
