from models.entities.SubjectTeacher import SubjectTeacher

class ModelSubjectTeacher:    

    @staticmethod
    def get_teacher_grade(db, teacher_id):
        try:
            cursor = db.connection.cursor()
            
            # Definir la consulta SQL
            query = """
                SELECT grados.id
                FROM teachers
                INNER JOIN subject_teacher ON subject_teacher.id_teacher = teachers.id
                INNER JOIN subjects ON subjects.id = subject_teacher.id_subject
                INNER JOIN grados ON grados.id = subjects.id_grado
                WHERE teachers.id = %s
                LIMIT 1
            """
            
            # Ejecutar la consulta pasando el teacher_id
            cursor.execute(query, (teacher_id,))
            
            # Recuperar el primer resultado
            grade = cursor.fetchone()  # Devuelve la primera fila
            cursor.close()  # Cerrar el cursor
            
            return grade

        except Exception as e:
            print(f"Error al obtener el grado del profesor: {e}")
            return None

    @staticmethod
    def get_subjects_by_teacher(db, teacher_id):
        try:
            cursor = db.connection.cursor()
            query = """
                SELECT s.id, s.nombre
                FROM subjects s
                INNER JOIN subject_teacher st ON s.id = st.id_subject
                WHERE st.id_teacher = %s
            """
            cursor.execute(query,(teacher_id,))
            subjects = cursor.fetchall()
            cursor.close()
            return subjects
        except Exception as e:
            print(f"Error al obtener materias del profesor: {e}")
            return []

    @staticmethod
    def get_subjects_by_grade_and_teacher(db, grade_id, teacher_id):
        try:
            cursor = db.connection.cursor()
            query = """
                SELECT s.id, s.nombre,
                    CASE WHEN st.id_teacher IS NOT NULL THEN 1 ELSE 0 END AS assigned
                FROM subjects s
                LEFT JOIN subject_teacher st ON s.id = st.id_subject AND st.id_teacher = %s
                WHERE s.id_grado = %s
            """
            cursor.execute(query, (teacher_id, grade_id))
            subjects = cursor.fetchall()
            cursor.close()

            # Transformar el resultado a un formato de diccionario
            return [{"id": row[0], "name": row[1], "assigned": bool(row[2])} for row in subjects]
        except Exception as e:
            print(f"Error al obtener materias por grado y profesor: {e}")
            return []


    @staticmethod
    def delete_by_teacher(db, teacher_id):
        try:
            cursor = db.connection.cursor()
            query = "DELETE FROM subject_teacher WHERE id_teacher = %s"
            cursor.execute(query, (teacher_id,))
            db.connection.commit()
        except Exception as e:
            print(f"Error al eliminar materias del docente: {e}")

    @staticmethod
    def add_subject_to_teacher(db, teacher_id, subject_id):
        try:
            cursor = db.connection.cursor()
            query = """
                INSERT INTO subject_teacher (id_teacher, id_subject)
                VALUES (%s, %s)
            """
            cursor.execute(query, (teacher_id, subject_id))
            db.connection.commit()
        except Exception as e:
            print(f"Error al agregar materia al docente: {e}")

    @staticmethod
    def delete_subjects_by_teacher(db, teacher_id):
        cursor = db.connection.cursor()
        try:
            # Eliminar todas las materias asociadas al docente
            cursor.execute("DELETE FROM subject_teacher WHERE id_teacher = %s", (teacher_id,))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise ex
        finally:
            cursor.close()