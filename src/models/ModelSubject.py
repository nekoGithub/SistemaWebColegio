from models.entities.Subject import Subject  

class ModelSubject:
    @classmethod
    def create_subject(cls, db, subject):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO subjects (nombre, id_grado)
                    VALUES (%s, %s)"""
            cursor.execute(sql, (
                subject.nombre,
                subject.id_grado,
                ))
            db.connection.commit()
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False

    @classmethod
    def update_subject(cls, db, subject):
        try:                   
            cursor = db.connection.cursor()
            sql = """UPDATE subjects
                    SET nombre = %s, id_grado = %s 
                    WHERE id = %s"""
            cursor.execute(sql, (
                subject.nombre,
                subject.id_grado,
                subject.id                
            ))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar Materias: {e}")
            return False

    @staticmethod
    def delete_subject(db, subject_id):
        cursor = db.connection.cursor()
        try:            
            cursor.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise ex
        finally:
            cursor.close()

    @classmethod
    def get_all_subjects(cls, db):
        try:            
            cursor = db.connection.cursor()                        
            sql = """
            SELECT subjects.id, subjects.nombre, grados.nombre AS grado_nombre , grados.ciclo AS grado_ciclo
            FROM subjects
            INNER JOIN grados ON subjects.id_grado = grados.id
            """                       
            cursor.execute(sql)                        
            subjects = cursor.fetchall()                        
            return subjects
        except Exception as ex:            
            raise Exception(ex)
        
    @staticmethod
    def get_by_id(db, subject_id):
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT s.id, s.nombre, s.id_grado, g.nombre, g.ciclo
            FROM subjects s
            JOIN grados g ON s.id_grado = g.id
            WHERE s.id = %s
        """, (subject_id,))
        result = cursor.fetchone()
        if result:
            return Subject(result[0], result[1], result[2], result[3], result[4])
        return None

    @staticmethod
    def get_subjects_by_grade(db, grade_id):
        # Consulta para obtener las materias de un grado
        query = """
            SELECT s.id, s.name
            FROM subjects s
            WHERE s.grade_id = %s
        """
        result = db.session.execute(query, (grade_id,))
        return result.fetchall()


    @staticmethod
    def get_subjects_by_grade(db, grade_id):
        try:
            cursor = db.connection.cursor()
            query = "SELECT id, nombre FROM subjects WHERE id_grado = %s"
            cursor.execute(query, (grade_id,))
            subjects = cursor.fetchall()
            cursor.close()
            return [{'id': row[0], 'name': row[1]} for row in subjects]
        except Exception as ex:
            print(f"Error al obtener las materias: {ex}")
            return []