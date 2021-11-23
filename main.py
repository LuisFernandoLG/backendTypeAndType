from logging import StreamHandler
from typing import Optional
from fastapi import FastAPI
from pydantic.main import BaseModel
from app.CategoriesController import CategoryController
from app.ExerciseController import ExerciseController
from fastapi.middleware.cors import CORSMiddleware
from app.ScoreController import ScoreController
from app.Session import SessionController
from app.UserController import UserController
from app.models.ExerciseMode import ExerciseModel
from app.models.ScoreModel import ScoreModel
from app.models.UserModel import UserModel

app = FastAPI()
exerciseDb = ExerciseController()
userDb = UserController()
scoreDb = ScoreController()
sessionDb = SessionController()
categoryDb = CategoryController()

origins = ["*"]

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
        "data": exercise
    }


@app.get("/admin/exercises")
def get_exercises_admin_view():
    data = exerciseDb.get_all_admin()
    return {
        "status": 202,
        "statusText": "Successful",
        "data": data
    }


@app.get("/exercises")
def get_exercises():
    data = exerciseDb.get_all()
    return {
        "status": 202,
        "statusText": "Successful",
        "data": data
    }


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
