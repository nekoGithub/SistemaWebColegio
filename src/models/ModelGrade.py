from models.entities.Grade import Grade  

class ModelGrade:
    @classmethod
    def create_grade(cls, db, grade):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO grados (nombre, ciclo)
                    VALUES (%s, %s)"""
            cursor.execute(sql, (
                grade.nombre,
                grade.ciclo,
                ))
            db.connection.commit()
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False

    @classmethod
    def update_grade(cls, db, grade):
        try:                   
            cursor = db.connection.cursor()
            sql = """UPDATE grados
                    SET nombre = %s, ciclo = %s 
                    WHERE id = %s"""
            cursor.execute(sql, (
                grade.nombre,
                grade.ciclo,
                grade.id                
            ))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar Grados: {e}")
            return False

    @staticmethod
    def delete_grade(db, grade_id):
        cursor = db.connection.cursor()
        try:            
            cursor.execute("DELETE FROM grados WHERE id = %s", (grade_id,))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise ex
        finally:
            cursor.close()

    @classmethod
    def get_all_grades(cls, db):
        try:            
            cursor = db.connection.cursor()                        
            sql = "SELECT * FROM grados"                        
            cursor.execute(sql)                        
            grades = cursor.fetchall()                        
            return grades
        except Exception as ex:            
            raise Exception(ex)
        
    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM grados WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return Grade(row[0], row[1], row[2])  
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error al obtener grado por ID: {ex}")

