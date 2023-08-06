from tuidbtv.controllers.MySQLController import MySQLController
from tuidbtv.controllers.PostgresController import PostgresController
from tuidbtv.controllers.SQLLiteController import SQLLiteController


class ControllerFactory:
    @staticmethod
    def getController(data):
        match data['connectionType']:
            case "postgresql":
                return PostgresController(data['database'], data['userName'], data['password'], data['hostName'],
                                          data['port'])

            case "mysql":
                return MySQLController(data['database'], data['userName'], data['password'], data['hostName'],
                                       data['port'])

            case "sqlite":
                return SQLLiteController(data['db_path'])
