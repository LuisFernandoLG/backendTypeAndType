from DbController import DbController


class UserController(DbController):
    def __init__(self):
        DbController.__init__(self)

    def add_new_user(self, name, surname, secondSurname, email, password, typeUser) -> bool:
        if(self.exist_user(email=email) == True):
            return False

        self.initialize_connection()
        query = f"""INSERT INTO users VALUES (0, '{name}', '{surname}', '{secondSurname}', '{email}', '{password}', {typeUser});"""
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


sc = UserController()

print(sc.add_new_user("Luis Fernando", "López",
      "Gutiérrez", "fer@gmail.com", "1234567890", 1))

# print(sc.exist_user("fer@gmail.com"))


# Necesitamos una vista en MYSQL para poder mostrar la info del usuario (:
