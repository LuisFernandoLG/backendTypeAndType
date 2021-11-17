import mysql.connector
from mysql.connector import Error, connect


class DbController():
    def __init__(self):
        self.host = 'boz0zkeoldaj4z0x4yjc-mysql.services.clever-cloud.com'
        self.database = 'boz0zkeoldaj4z0x4yjc'
        self.user = 'uabk4vz4e2r6vwhk'
        self.password = '3MITTMqtVflvBSsyDeD5'
        self.connection = None
        self.cursor = None

    def initialize_connection(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password)
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
            self.connection.close()
            print("MySQL connection is closed")
