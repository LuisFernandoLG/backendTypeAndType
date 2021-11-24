from app.DbController import DbController


class ExerStatusController(DbController):
    def __init__(self):
        DbController.__init__(self)

    def get_all(self):
        self.initialize_connection()
        query = "SELECT * FROM statuses"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.close_connection()
        return self._format_get_all(data)

    def _format_get_all(self, data):
        data_formated = []
        for cate in data:
            data_formated.append({
                "id": cate[0],
                "name": cate[1]
            })
        return data_formated
