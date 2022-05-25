from imp import reload
from logging import StreamHandler
from typing import Optional
from fastapi import FastAPI
from pydantic.main import BaseModel
import uvicorn
from app.CategoriesController import CategoryController
from app.CourseController import CourseController
from app.DifficultiesController import DifficultyController
from app.ExerStatusController import ExerStatusController
from app.ExerciseController import ExerciseController
from fastapi.middleware.cors import CORSMiddleware
from app.ScoreController import ScoreController
from app.Session import SessionController
from app.UserController import UserController
from app.models.ExerciseMode import ExerciseModel
from app.models.ScoreModel import ScoreModel
from app.models.UserModel import UserModel
from exampleData import exercises
# Something?
app = FastAPI()
exerciseDb = ExerciseController()
userDb = UserController()
scoreDb = ScoreController()
sessionDb = SessionController()
categoryDb = CategoryController()
difficultyDB = DifficultyController()
exerStatusDb = ExerStatusController()
courseDb = CourseController()

origins = [
    "*",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_basic_information():
    return {"Hello": "World"}


@app.post("/admin/exercise")
def add_exercise(exercise: ExerciseModel):
    response = exerciseDb.add(exercise)
    return {
        "status": 202,
        "statusText": "Successful",
        "data": exercise
    }


@app.put("/admin/exercise")
def update_exercise(exercise: ExerciseModel):
    response = exerciseDb.update(exercise)
    return {
        "status": 202,
        "statusText": "Successful",
        "data": response
    }


@app.get("/admin/exercises")
def get_exercises_admin_view():
    adminExercises = exerciseDb.get_all_admin()
    categories = categoryDb.get_all()
    difficulties = difficultyDB.get_all()
    statuses = exerStatusDb.get_all()

    return {
        "status": 202,
        "statusText": "Successful",
        "data": {
            "exercises": adminExercises,
            "categories": categories,
            "difficulties": difficulties,
            "statuses": statuses
        }
    }


@app.get("/exercises")
def get_exercises():
    data = exerciseDb.get_all()
    return {
        "status": 202,
        "statusText": "Successful",
        "data": data
    }


@app.get("/something")
def get_exercise():
    return {"message": "hi"}


@app.get("/exercise/{id}")
def get_exercise(id):
    data = exerciseDb.get(id)
    return {
        "status": 202,
        "statusText": "Successful",
        "data": data
    }


@app.post("/signIn")
def sign_in_user(user: UserModel):
    response = userDb.add_new_user(user)
    if(response == False):
        return {
            "status": 201,
            "statusText": "Correo ya registrado!",
        }
    else:
        return {
            "status": 202,
            "statusText": "Successful",
            "data": user
        }


@app.post("/score")
async def complete_exercises(score: ScoreModel):
    response = await scoreDb.add(score)
    return {
        "status": 202,
        "statusText": "Successful",
        "data": score,
        "response": response
    }


@app.get("/score/{userId}")
def get_score(userId):
    data = scoreDb.get_scores(userId)
    return {
        "status": 202,
        "statusText": "Successful",
        "data": data,
    }


@app.get("/categories")
def get_categories():
    dataList = categoryDb.get_all()
    return {
        "status": 202,
        "data": {"categories": dataList}
    }


@app.get("/exercises/search")
def get_score(query: str = "", category: Optional[int] = -1):
    data = []
    if(category == -1):
        print("SIN CATEGORIA")
        print(f"""query:{query}""")
        print(f"""category:{category}""")
        data = exerciseDb.get_by_query(query)
    else:
        print("CON CATEGORIA")
        print(f"""query:{query}""")
        print(f"""category:{category    }""")
        data = exerciseDb.get_by_query_and_category(query, category)

    return {
        "status": 202,
        "statusText": "Successful",
        "data": data
    }


class UserSession(BaseModel):
    email: str
    password: str


@app.post("/logIn")
def get_session(userSession: UserSession):
    response = sessionDb.logIn(userSession.email, userSession.password)

    print(response)
    if(response == 1):
        user = userDb.get_user(userSession.email)
        return {"status": "201", "statusText": "Login éxitoso", "data": {"user": user}}
    if(response == 0):
        return {"status": "202", "statusText": "Contraseña incorrecta"}
    if(response == 3):
        return {"status": "202", "statusText": "Correo no registrado"}


@app.get("/ranking")
def get_ranking():
    data = scoreDb.get_ranking()
    return {
        "status": 202,
        "data": data
    }


@app.get("/stadistics/{idUser}")
def get_ranking(idUser):
    data = scoreDb.get_stadistics(idUser)
    return {
        "status": 202,
        "data": data
    }


@app.get("/englishExercises/{courseId}/{exerciseId}")
def get_english_exercises(courseId, exerciseId):
    print(exercises)
    return {"data": exercises}


class UserM(BaseModel):
    userName: str
    email: str
    password: str
    imageProfile: str


@app.put("/user")
def update_user(userM: UserM):
    response = userDb.update_user(
        userM.userName, userM.email, userM.password, userM.imageProfile)
    return {"status": 202}


class RecoverPassModel(BaseModel):
    email: str


@app.post("/recover/pass")
def update_user(recoverPassModel: RecoverPassModel):
    response = userDb.recover_pass(recoverPassModel.email)
    return {"response": 202, "data": response}


@app.get("/course/{courseId}")
def getExercisesFromCourse(courseId):
    response = courseDb.getCourse(courseId)
    return {"status": 202, "data" : response}

class CourseModel(BaseModel):
    id: int
    name: str
    description: str
    courseType: int
    status: int


@app.post("/course")
def addCourse(courseModel : CourseModel):
    response = courseDb.addCourse(courseModel)
    return {"status": 202, "data" : response}

@app.put("/course")
def addCourse(courseModel : CourseModel):
    response = courseDb.updateCourse(courseModel)
    return {"status": 202, "data" : response}




@app.get("/courses/user/{userId}")
def getAllCourses(userId):
    response = courseDb.get_all_courses(userId)
    return {"status":"202", "data": response}



@app.get("/coursesTemplate")
def getCoursesTemplate():
    response = courseDb.get_coursesTemplate()
    return {"status":"202", "data": response}

@app.get("/exercisesMarked/{courseId}/{userId}")
def getCoursesTemplatex(courseId, userId):
    response = courseDb.get_abc_exercises_marked(courseId, userId)
    return {"status":"202", "data": response}


class MecaExercise(BaseModel):
    mecaId: int
    title: str
    textContent: str
    status: int

@app.put("/course/mecaExercise")
def updateMecaExercisex(mecaExercise : MecaExercise):
    response = courseDb.updateMecaExercise(mecaExercise)
    return {"status":"202", "data": response}

@app.post("/course/mecaExercise/{courseId}")
def addMecaExercise(courseId, mecaExercise : MecaExercise):
    response = courseDb.addMecaExercise(courseId, mecaExercise)
    return {"status":"202", "data": response}

class AbcExercise(BaseModel):
    idQuestion: int
    title: str
    question: str
    correctAnswer: str
    secondAnswer : str
    tirthAnswer : str
    status: int

@app.put("/course/abcExercise")
def updateAbcExercisex(abcExercise : AbcExercise):
    response = courseDb.updateAbcExercise(abcExercise)
    return {"status":"202", "data": response}

@app.post("/course/abcExercise/{courseId}")
def addAbcExercise(courseId, abcExercise : AbcExercise):
    response = courseDb.addAbcExercise(courseId, abcExercise)
    return {"status":"202", "data": response}

class ExerciseMarket(BaseModel):
    courseId : int
    exerciseId: int
    userId : int
    

@app.post("/course/exercise/markascompleted")
def addAbcExercise(marker : ExerciseMarket):
    response = courseDb.markExerciseFromCourseCompleted(marker.courseId, marker.exerciseId, marker.userId )
    return {"status":"202", "data": response}





if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
