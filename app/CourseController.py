from inspect import iscode
import random

from fastapi import Query
from app.DbController import DbController
import shortuuid


class CourseController(DbController):
    def __init__(self):
        DbController.__init__(self)

    def get_abc_exercises(self, courseId):
        self.initialize_connection()
        # Get abc exercises from a specific course
        abcQuery = f"""SELECT questions.*, answers2.correctAnswer, answers2.secondAnswer, answers2.tirthAnswer, coursesWithExercises.courseId, coursesWithExercises.exerciseType FROM questions, answers2, coursesWithExercises
WHERE coursesWithExercises.courseId = {courseId} AND coursesWithExercises.exerciseId = questions.idQuestion AND questions.idQuestion = answers2.questionId;
"""
        self.cursor.execute(abcQuery)
        abcExercises = self.cursor.fetchall()
        abcExercises = self.format_abc_exercise(abcExercises)

        self.close_connection()
        return abcExercises

    def get_meca_exercises(self, courseId):
        self.initialize_connection()

        mecaQuery = f"""SELECT mecaExercises.*, coursesWithExercises.courseId, coursesWithExercises.exerciseType  FROM mecaExercises, coursesWithExercises
        WHERE coursesWithExercises.exerciseId = mecaExercises.mecaId AND coursesWithExercises.courseId = {courseId} AND coursesWithExercises.exerciseType = 1;"""
        self.cursor.execute(mecaQuery)
        mecaData = self.cursor.fetchall()
        mecaData = self.format_meca_exercises(mecaData)

        self.close_connection()
        return mecaData

    def getCourse(self, courseId):
        abcExercises = self.get_abc_exercises(courseId)
        mecaData = self.get_meca_exercises(courseId)
        return [*abcExercises, *mecaData]

    
    def addCourse(self, courseModel):
        self.initialize_connection()
        query = f"""INSERT INTO courses VALUES (NULL, '{courseModel.name}', '{courseModel.description}', 2, {courseModel.status})"""
        self.cursor.execute(query)
        self.connection.commit()
        self.close_connection()
        return courseModel

    
    def updateCourse(self, courseModel):
        self.initialize_connection()
        query = f"""UPDATE courses SET name = '{courseModel.name}', description = '{courseModel.description}', status = {courseModel.status} WHERE id = {courseModel.id}"""
        self.cursor.execute(query)
        self.connection.commit()
        self.close_connection()
        return courseModel

    

    

    def get_coursesTemplate(self):
        self.initialize_connection()
        query = "SELECT * FROM courses;"
        self.cursor.execute(query)
        courses = self.cursor.fetchall()
        coursesData = []
        for course in courses:
            # abcData = self.get_abc_exercises(course[0])
            # mecaData = self.get_meca_exercises(course[0])
            coursesData.append({
                "courseId": course[0],
                "title": course[1],
                "description": course[2],
                "categoryCourse": course[3],
            })

        self.close_connection()
        print(coursesData)
        return coursesData

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

    def updateMecaExercise(self, mecaExercise):
        self.initialize_connection()
        result = self.cursor.callproc(
            'updateMecaExercise', args=(mecaExercise.mecaId, mecaExercise.title, mecaExercise.textContent, mecaExercise.status))

        self.connection.commit()
        self.close_connection()
        return mecaExercise

    
    def addMecaExercise(self, courseId, mecaExercise):
        self.initialize_connection()
        result = self.cursor.callproc(
            'addMecaExercise', args=(courseId, 1, mecaExercise.title, mecaExercise.textContent, mecaExercise.status))

        self.connection.commit()
        self.close_connection()
        return mecaExercise
    
    
    def addAbcExercise(self, courseId, abcExercise):
        self.initialize_connection()
        result = self.cursor.callproc(
            'addAbcExerciseToCourse', args=(courseId, 2, abcExercise.title, abcExercise.question, abcExercise.correctAnswer, abcExercise.secondAnswer, abcExercise.tirthAnswer, abcExercise.status))

        self.connection.commit()
        self.close_connection()
        return abcExercise

    def updateAbcExercise(self, abcExercise):
        self.initialize_connection()
        result = self.cursor.callproc(
            'updateAbcExercise', args=(abcExercise.idQuestion, abcExercise.title, abcExercise.question, abcExercise.correctAnswer, abcExercise.secondAnswer, abcExercise.tirthAnswer, abcExercise.status))

        self.connection.commit()
        self.close_connection()
        return abcExercise
    


    



    def format_abc_exercise(self, exercises):
        allExercises = []
        for exercise in exercises:
            answers = self._get_random_position_of_answers(
                [exercise[7], exercise[8], exercise[9]])
            
            # answers = ([exercise[7], exercise[8], exercise[9]])


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
        # radnomAnswers = random.sample(answers, len(answers))
        return answers

    def format_meca_exercises(self, exercises):
        allExercises = []
        for exercise in exercises:
            allExercises.append({
                "id": exercise[0],
                "title": exercise[1],
                # "points": exercise[2],
                "textContent": exercise[2],
                # "time": exercise[4],
                "status": exercise[3],
                # "idCategory": exercise[6],
                # "difficulty": exercise[7],
                "courseId": exercise[4],
                "exerciseType": exercise[5],
            })
        return allExercises
