from datetime import datetime
from models.entities.Teacher import Teacher  # Importamos la clase Teacher

class ModelTeacher:
    @classmethod
    def create_teacher(cls, db, teacher):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO teachers (nombres, apellidos, sexo, ci, num_celular, fecha_ingreso, estado, id_user)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                teacher.nombres,
                teacher.apellidos,
                teacher.sexo,
                teacher.ci,
                teacher.num_celular,
                teacher.fecha_ingreso,
                teacher.estado,
                teacher.id_user 
            ))
            db.connection.commit()
            # Obtener el id del último registro insertado
            teacher_id = cursor.lastrowid  # Esto devuelve el ID del nuevo registro
            return teacher_id  # Retornamos el ID para usarlo fuera de la función
        except Exception as ex:
            print(f"Error: {ex}")
            return False
    
    @classmethod
    def update_teacher(cls, db, teacher):
        try:                   
            cursor = db.connection.cursor()
            sql = """UPDATE teachers
                    SET nombres = %s, apellidos = %s, sexo = %s, ci = %s, num_celular = %s, fecha_ingreso = %s, estado = %s, update_at = %s
                    WHERE id = %s"""
            cursor.execute(sql, (
                teacher.nombres,
                teacher.apellidos,
                teacher.sexo,
                teacher.ci,
                teacher.num_celular,
                teacher.fecha_ingreso,
                teacher.estado,
                datetime.now(),  
                teacher.id
            ))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar docente: {e}")
            return False

    @staticmethod
    def delete_teacher(db, teacher_id):
        cursor = db.connection.cursor()
        try:            
            cursor.execute("UPDATE teachers SET estado = 'inactivo' WHERE id = %s", (teacher_id,))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise ex
        finally:
            cursor.close()

    @classmethod
    def get_all_teachers(cls, db):
        try:            
            cursor = db.connection.cursor()                        
            sql = "SELECT * FROM teachers WHERE estado='activo'"                        
            cursor.execute(sql)                        
            teachers = cursor.fetchall()                        
            return teachers
        except Exception as ex:            
            raise Exception(ex)
        
    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM teachers WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row:
                return Teacher(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])  # Retorna el objeto User
            else:
                return None
        except Exception as ex:
            raise Exception(f"Error al obtener usuario por ID: {ex}")

    @staticmethod
    def get_subjects_by_teacher(db, teacher_id):
        """
        Obtiene las materias asociadas a un profesor por su ID.

        :param db: Conexión o sesión de la base de datos.
        :param teacher_id: ID del profesor.
        :return: Lista de materias asociadas al profesor.
        """
        try:
            query = """
                SELECT m.id, m.name 
                FROM subjects AS m
                INNER JOIN teacher_subjects AS ts ON ts.subject_id = m.id
                WHERE ts.teacher_id = :teacher_id
            """
            result = db.execute(query, {"teacher_id": teacher_id})
            subjects = result.fetchall()
            return subjects
        except Exception as e:
            print(f"Error al obtener materias para el profesor con ID {teacher_id}: {e}")
            return []