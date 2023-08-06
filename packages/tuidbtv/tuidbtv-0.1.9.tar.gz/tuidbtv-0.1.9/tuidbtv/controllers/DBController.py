class DBController():
    def getSchemaNames(self) -> list[str]:
        pass

    def getTableNamesBySchema(self, schemaName: str) -> list[str]:
        pass

    def getTablePreview(self, schemaName: str, tableName: str, order_by="", desc=False) -> list[dict]:
        pass

    def executeQuery(self, queryText: str) -> list[dict]:
        pass

    def executeQueryWithHeaders(self, queryText: str):
        pass

    @staticmethod
    def get_connection_form():
        pass