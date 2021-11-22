from app.DbController import DbController
from app.models.ExerciseMode import ExerciseModel


class ExerciseController(DbController):
    def __init__(self):
        DbController.__init__(self)

    def add(self, exercise: ExerciseModel):
        self.initialize_connection()
        query = f"""INSERT INTO exercises VALUES (NULL, "{exercise.title}", {exercise.points}, "{exercise.text_content}", {exercise.time},{exercise.status},{exercise.category},{exercise.difficulty});"""
        self.cursor.execute(query)
        self.connection.commit()
        self.close_connection()
        return True

    def delete(self, id):
        self.initialize_connection()
        query = f"""DELETE FROM exercises WHERE idExercise = {id} """
        self.cursor.execute(query)
        self.connection.commit()
        self.close_connection()
        return True

    def update(self):
        pass

    def get(self, id):
        self.initialize_connection()
        query = f"""SELECT idExercise, title, textContent, points, time FROM exercises WHERE idExercise = {id};"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.close_connection()
        return self.format_exercise(data[0])

    def format_exercise(self, exercise):
        return {
            "id": exercise[0],
            "title": exercise[1],
            "textContent": exercise[2],
            "points": exercise[3],
            "time": exercise[4],
        }

    def get_all(self):
        self.initialize_connection()
        query = "select * from exercisesView;"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        print(data)
        self.close_connection()
        return self.format_get_all(data)

    def format_get_all(self, exercises: list) -> list:
        formated_data = []
        for exercise in exercises:
            formated_exercise = {
                "id": exercise[0],
                "title": exercise[1],
                "textContent": exercise[2],
                "category": exercise[3],
                "difficulty": exercise[4],
            }
            formated_data.append(formated_exercise)

        return formated_data

    def get_by_query(self, query):
        self.initialize_connection()
        results = self.cursor.callproc(
            'searchByQuery', (query,)
        )
        results = [r.fetchall() for r in self.cursor.stored_results()][0]
        self.close_connection()
        return self.format_get_all(results)

    def get_by_query_and_category(self, query, idCategory):
        self.initialize_connection()
        results = self.cursor.callproc(
            'searchByQueryAndCategory', args=(query, idCategory)
        )
        results = [r.fetchall() for r in self.cursor.stored_results()][0]
        self.close_connection()
        return self.format_get_all(results)
