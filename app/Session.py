from app.DbController import DbController


class SessionController(DbController):
    def __init__(self):
        DbController.__init__(self)

    # Possible Responses
    # 1 means OK
    # 2 means wrong password
    # 3 means email doesn't exist
    def logIn(self, email, password) -> bool:
        self.initialize_connection()
        result = self.cursor.callproc(
            'logIn', args=(email, password, (0)))
        x = result[2]
        self.connection.commit()
        self.close_connection()
        return x
