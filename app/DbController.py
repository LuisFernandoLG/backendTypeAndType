import mysql.connector
from mysql.connector import Error, connect


class DbController():
    def __init__(self):
        self.host = 'b5izkncghqfl1swxkukj-mysql.services.clever-cloud.com'
        self.database = 'b5izkncghqfl1swxkukj'
        self.user = 'uabk4vz4e2r6vwhk'
        self.password = '3MITTMqtVflvBSsyDeD5'
        self.port = "21164"
        self.connection = None
        self.cursor = None

    def initialize_connection(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            if self.connection.is_connected():
                self.initialize_cursor()
                return True
            else:
                print("No fue exitosa")
                return False

        except Error as e:
            print("Error while connecting to MySQL", e)
            return False

    def initialize_cursor(self):
        self.cursor = self.connection.cursor()

    def close_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")
