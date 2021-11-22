from app.models.UserModel import UserModel
from app.DbController import DbController


class UserController(DbController):
    def __init__(self):
        DbController.__init__(self)

    def add_new_user(self, user: UserModel) -> bool:
        if(self.exist_user(user.email) == True):
            return False

        self.initialize_connection()
        query = f"""INSERT INTO users VALUES (NULL, '{user.name}', '{user.surname}', '{user.second_surname}', '{user.email}', '{user.password}', 2);"""
        self.cursor.execute(query)
        self.connection.commit()
        self.close_connection()
        return True

    def exist_user(self, email) -> bool:
        self.initialize_connection()
        query = f"""SELECT COUNT(idUser) as total FROM users WHERE email='{email}'"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.close_connection()

        if(data[0][0] == 1):
            return True
        else:
            return False

    def get_user(self, email) -> dict:
        self.initialize_connection()
        query = f"""SELECT idUser, name, surname, typeUser, email, password FROM users WHERE email='{email}'"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.close_connection()
        return self._formar_user(data[0])

    def _formar_user(self, userData):
        return {
            "id": userData[0],
            "name": userData[1],
            "surname": userData[2],
            "typeUser": userData[3],
            "email": userData[4],
            "password": userData[5],
        }


# sc = UserController()

# print(sc.add_new_user("Luis Fernando", "López",
#       "Gutiérrez", "fer@gmail.com", "1234567890", 1))

# print(sc.exist_user("fer@gmail.com"))


# Necesitamos una vista en MYSQL para poder mostrar la info del usuario (:
