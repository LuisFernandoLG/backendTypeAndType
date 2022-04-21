from inspect import iscode
import random
from winreg import QueryValue
from app.DbController import DbController
import shortuuid


class CourseController(DbController):
    def __init__(self):
        DbController.__init__(self)

    def get_abc_exercises(self, courseId):
        self.initialize_connection()
        # Get abc exercises from a specific course
        abcQuery = f"""SELECT questions.*, answers2.correctAnswer, answers2.secondAnswer, answers2.tirthAnswer, coursesWithExercises.courseId, coursesWithExercises.exerciseType FROM questions, answers2, coursesWithExercises
WHERE coursesWithExercises.courseId = {courseId} AND coursesWithExercises.exerciseId = questions.idQuestion AND questions.idQuestion = answers2.id;
"""
        self.cursor.execute(abcQuery)
        abcExercises = self.cursor.fetchall()
        abcExercises = self.format_abc_exercise(abcExercises)

        self.close_connection()
        return abcExercises

    def get_meca_exercises(self, courseId):
        self.initialize_connection()

        mecaQuery = f"""SELECT exercises.*, coursesWithExercises.courseId, coursesWithExercises.exerciseType  FROM exercises, coursesWithExercises
WHERE coursesWithExercises.exerciseId = exercises.idExercise AND coursesWithExercises.courseId = {courseId};"""
        self.cursor.execute(mecaQuery)
        mecaData = self.cursor.fetchall()
        mecaData = self.format_meca_exercises(mecaData)

        self.close_connection()
        return mecaData

    def getCourse(self, courseId):
        abcExercises = self.get_abc_exercises(courseId)
        mecaData = self.get_meca_exercises(courseId)
        return [*abcExercises, *mecaData]

    def get_all_courses(self):
        self.initialize_connection()
        query = "SELECT * FROM courses;"
        self.cursor.execute(query)
        courses = self.cursor.fetchall()
        self.close_connection()

        data_formated = self._get_exercises_from_course_formated(courses)
        return data_formated

    def _get_exercises_from_course_formated(self, courses):
        coursesData = []
        for course in courses:
            abcData = self.get_abc_exercises(course[0])
            mecaData = self.get_meca_exercises(course[0])
            coursesData.append({
                "courseId": course[0],
                "categoryName": course[1],
                "description": course[2],
                "courseType": course[3],
                "exercises": [*abcData, *mecaData],
            })

        return coursesData

    def format_abc_exercise(self, exercises):
        allExercises = []
        for exercise in exercises:
            answers = self._get_random_position_of_answers(
                [exercise[7], exercise[8], exercise[9]])
            allExercises.append({
                "id": exercise[0],
                "title": exercise[1],
                "question": exercise[2],
                "points": exercise[3],
                "idDificulty": exercise[4],
                "idStatus": exercise[5],
                "idCategory": exercise[6],
                "answers": answers,
                "couseId": exercise[10],
                "exerciseType": exercise[11],
                "isDone": False})

        return allExercises

    def _get_random_position_of_answers(self, answers: list):
        answer1 = {"id": shortuuid.uuid(
        ), "content": answers[0], "isCorrect": True}
        answer2 = {"id": shortuuid.uuid(
        ), "content": answers[1], "isCorrect": False}
        answer3 = {"id": shortuuid.uuid(
        ), "content": answers[2], "isCorrect": False}

        answers = [answer1, answer2, answer3]
        radnomAnswers = random.sample(answers, len(answers))
        return radnomAnswers

    def format_meca_exercises(self, exercises):
        allExercises = []
        for exercise in exercises:
            allExercises.append({
                "id": exercise[0],
                "title": exercise[1],
                "points": exercise[2],
                "textContent": exercise[3],
                "time": exercise[4],
                "status": exercise[5],
                "idCategory": exercise[6],
                "difficulty": exercise[7],
                "courseId": exercise[8],
                "exerciseType": exercise[9],
            })
        return allExercises
