from models.entities.Note import Note

class ModelNote:
    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, nota1, nota2, nota3, nota4, promedio, observaciones FROM stundent_notes WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return Note(row[0], row[1], row[2], row[3], row[4], row[5], row[6])  
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error al obtener Notas por ID: {ex}")