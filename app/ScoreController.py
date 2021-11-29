from fastapi.params import Query
from app.DbController import DbController
from app.helpers import hasKey
from app.models.ExerciseMode import ExerciseModel
from app.models.ScoreModel import ScoreModel


class ScoreController(DbController):
    def __init__(self):
        DbController.__init__(self)

    async def add(self, score: ScoreModel):
        self.initialize_connection()
        self.cursor.callproc('registerScore', args=(
            score.user_id, score.exercise_id, score.total_score, score.time_taken))
        self.connection.commit()
        self.close_connection()
        return True

    def get_scores(self, idUser):
        self.initialize_connection()
        self.cursor.execute(f"SELECT * FROM scores WHERE user = {idUser};")
        data = self.cursor.fetchall()
        self.close_connection()
        return self._format_score_user(data)

    def _format_score_user(self, data):
        data_formated = []
        for score in data:
            data_formated.append({
                "scoreId": score[0],
                "date": score[1],
                "totalScore": score[2],
                "userId": score[3],
                "exerciseId": score[4],
                "timeTaken": score[5],
                "isCompleted": score[6],

            })
        return data_formated

    def get_ranking(self):
        self.initialize_connection()
        query = "SELECT * FROM GetScores;"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.close_connection()
        return self._format_ranking(data)

    def _format_ranking(self, scores):
        formated_data = []
        for scoreUser in scores:
            formated_data.append({
                "id": scoreUser[0],
                "name": scoreUser[1],
                "lastName": scoreUser[2],
                "totalScore": scoreUser[3],

            })
        return formated_data

    def get_stadistics(self, idUser):
        self.initialize_connection()
        results = self.cursor.callproc(
            'getStadistics', (idUser,)
        )
        results = [r.fetchall() for r in self.cursor.stored_results()][0]
        print(results)
        self.close_connection()
        return self._format_stadistics(results)

    def _format_stadistics(self, data):
        data_formated = {}
        for i in data:
            exists = hasKey(data_formated, str(i[0]))
            if(exists == True):
                data_formated[str(i[0])] = [*data_formated[str(i[0])], {
                    "exerciseId": i[0],
                    "totalScore": i[1],
                    "userId": i[2],
                    "lastTimeTaken": i[3],
                    "status": i[4]
                }]

            else:
                data_formated[str(i[0])] = [{
                    "exerciseId": i[0],
                    "totalScore": i[1],
                    "userId": i[2],
                    "lastTimeTaken": i[3],
                    "status": i[4]
                }]

        return list(data_formated.values())
