from models.entities.Student import Student  

class ModelStudent:
    @classmethod
    def create_student(cls, db, student):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO students (nombres, apellidos, ci, genero, num_celular, fecha_nacimiento, estado, fecha_ingreso, id_user)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                student.nombres,
                student.apellidos,
                student.ci,
                student.genero,
                student.num_celular,
                student.fecha_nacimiento,
                student.estado,
                student.fecha_ingreso,
                student.id_user,
                ))
            db.connection.commit()
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False
        
    @classmethod
    def update_student(cls, db, student):
        try:                   
            cursor = db.connection.cursor()
            sql = """UPDATE students
                    SET nombres = %s, apellidos = %s, ci = %s, genero = %s, num_celular = %s, fecha_nacimiento = %s, estado = %s, fecha_ingreso = %s, id_user = %s 
                    WHERE id = %s"""
            cursor.execute(sql, (
                student.nombres,
                student.apellidos,
                student.ci,
                student.genero,
                student.num_celular,
                student.fecha_nacimiento,
                student.estado,
                student.fecha_ingreso,
                student.id_user,                
                student.id,                
            ))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar Estudiantes: {e}")
            return False

    @staticmethod
    def delete_student(db, student_id):
        cursor = db.connection.cursor()
        try:            
            cursor.execute("UPDATE students SET estado = 'inactivo' WHERE id = %s", (student_id,))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise ex
        finally:
            cursor.close()

    @classmethod
    def get_all_students(cls, db):
        try:            
            cursor = db.connection.cursor()                        
            sql = """
            SELECT *
            FROM Students
            WHERE estado="activo"
            ORDER BY id DESC
            """                       
            cursor.execute(sql)                        
            sections = cursor.fetchall()                        
            return sections
        except Exception as ex:            
            raise Exception(ex)
        
    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM students WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return Student(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])  
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error al obtener Estudiantes por ID: {ex}")
