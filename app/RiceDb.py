from app.DbController import DbController


class RiceDb(DbController):
    def __init__(self):
        DbController.__init__(self)

    def get_all(self, userId = 0):
        self.initialize_connection()
        self.cursor.callproc('getAllRicesWithDoneOnes', (userId,))
        results = [r.fetchall() for r in self.cursor.stored_results()][0]
        self.close_connection()

        data = self._format_get_all(results)

        return data

    

    def _format_get_all(self, data):
        data_formated = []
        for item in data:
            data_formated.append({
                "id": item[0],
                "title": item[1],
                "description": item[2],
                "difficulty": item[3],
                "neckColor": item[4],
                "difficultyId": item[5],
                "isDone": item[6]
            })
        return data_formated

    def get_exercise(self, riceId):
        self.initialize_connection()
        query = f"""SELECT rices.*, difficulties.Name_D FROM rices, difficulties WHERE id = {riceId} AND rices.difficultyId = difficulties.idDifficulty;"""
        self.cursor.execute(query)
        data = self.cursor.fetchall()

        return self._format_exercise(data[0])

    def _format_exercise(self, item):
            return {
                "id": item[0],
                "title": item[1],
                "description": item[2],
                "difficultyId": item[3],
                "neckColor": item[4],
                "status": item[5],
                "difficulty": item[6],
            }

    def markExerciseAsDone(self, riceExercise):
        self.initialize_connection()
        result = self.cursor.callproc(
            'markRiceDone', args=(riceExercise.riceId, riceExercise.userId))

        self.connection.commit()
        self.close_connection()
        return True


    
