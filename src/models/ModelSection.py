from models.entities.Section import Section  

class ModelSection:
    @classmethod
    def create_section(cls, db, section):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO sections (nombre, id_grado)
                    VALUES (%s, %s)"""
            cursor.execute(sql, (
                section.nombre,
                section.id_grado,
                ))
            db.connection.commit()
            return True
        except Exception as ex:
            print(f"Error: {ex}")
            return False

    @classmethod
    def update_section(cls, db, section):
        try:                   
            cursor = db.connection.cursor()
            sql = """UPDATE sections
                    SET nombre = %s, id_grado = %s 
                    WHERE id = %s"""
            cursor.execute(sql, (
                section.nombre,
                section.id_grado,
                section.id                
            ))
            db.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar Secciones: {e}")
            return False

    @staticmethod
    def delete_section(db, section_id):
        cursor = db.connection.cursor()
        try:            
            cursor.execute("DELETE FROM sections WHERE id = %s", (section_id,))
            db.connection.commit()
        except Exception as ex:
            db.connection.rollback()
            raise ex
        finally:
            cursor.close()

    @classmethod
    def get_all_sections(cls, db):
        try:            
            cursor = db.connection.cursor()                        
            sql = """
            SELECT sections.id, sections.nombre, grados.nombre AS grado_nombre , grados.ciclo AS grado_ciclo
            FROM sections
            INNER JOIN grados ON sections.id_grado = grados.id
            """                       
            cursor.execute(sql)                        
            sections = cursor.fetchall()                        
            return sections
        except Exception as ex:            
            raise Exception(ex)
        
    @staticmethod
    def get_by_id(db, section_id):
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT s.id, s.nombre, s.id_grado, g.nombre, g.ciclo
            FROM sections s
            JOIN grados g ON s.id_grado = g.id
            WHERE s.id = %s
        """, (section_id,))
        result = cursor.fetchone()
        if result:
            return Section(result[0], result[1], result[2], result[3], result[4])
        return None

