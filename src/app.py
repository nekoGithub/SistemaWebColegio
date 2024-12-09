from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,send_file, make_response
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from reportlab.pdfgen import canvas
from io import BytesIO
from io import BytesIO
import os

from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelTeacher import ModelTeacher
from models.ModelGrade import ModelGrade
from models.ModelSection import ModelSection
from models.ModelSubject import ModelSubject
from models.ModelSubjectTeacher import ModelSubjectTeacher
from models.ModelStudent import ModelStudent
from models.ModelNote import ModelNote

# Entities:
from models.entities.User import User
from models.entities.Teacher import Teacher
from models.entities.Grade import Grade
from models.entities.Section import Section
from models.entities.Subject import Subject
from models.entities.SubjectTeacher import SubjectTeacher
from models.entities.Student import Student
from models.entities.Note import Note

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        user = User(0, usuario, contrasena)  
        logged_user = ModelUser.login(db, user)

        if logged_user: 
            login_user(logged_user)
            print(logged_user.rol)            
            if logged_user.rol == 'administrador':
                return redirect(url_for('home'))  
            elif logged_user.rol == 'docente':
                return redirect(url_for('docente_home'))  
            else:
                flash("Rol no reconocido. Contacte al administrador.", 'danger')
                return redirect(url_for('login'))

        else:
            flash("Usuario o contraseña incorrectos.", 'danger')
            return render_template('auth/login.html')

    return render_template('auth/login.html')



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/docente_home')
def docente_home():
    return render_template('docente_home.html')


## Usuarios CRUD
@app.route('/users')
def users():
    try:
        users = ModelUser.get_all_users(db)          
        return render_template('users/users.html', users=users)
    except Exception as ex:
        flash("Ocurrió un error al recuperar los usuarios.")
        return redirect(url_for('home'))

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        nombre_completo = request.form['nombre_completo']
        rol = request.form['rol']  # Campo para el rol

        print(f"Datos recibidos: {usuario}, {contrasena}, {nombre_completo}, {rol}")
                
        user = User(0, usuario, contrasena, nombre_completo=nombre_completo, rol=rol, estado="activo")
        
        if ModelUser.create_user(db, user):
            flash('Usuario creado exitosamente.', 'success')
            return redirect(url_for('users'))
        else:
            flash('Error al crear el usuario.', 'danger')
    
    return render_template('users/create_user.html')



@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = ModelUser.get_by_id(db, user_id)
    
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        nombre_completo = request.form['nombre_completo']
        rol = request.form['rol'] 
                
        if contrasena:
            contrasena_encriptada = generate_password_hash(contrasena)
        else:
            contrasena_encriptada = user.contrasena
                
        updated_user = User(user.id, usuario, contrasena_encriptada, nombre_completo, rol=rol, estado=user.estado)

        if ModelUser.update_user(db, updated_user):
            flash('Usuario actualizado exitosamente.', 'success')
            return redirect(url_for('users'))
        else:
            flash('Error al actualizar el usuario.', 'danger')
            return redirect(url_for('edit_user', user_id=user.id))

    return render_template('users/edit_user.html', user=user)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        user = ModelUser.get_by_id(db, user_id)  
        if user:            
            ModelUser.delete_user(db, user_id)
            flash("Usuario eliminado exitosamente.", 'success')
        else:
            flash("Usuario no encontrado.", 'danger')
    except Exception as ex:
        flash(f"Ocurrió un error: {ex}", 'danger')
    return redirect(url_for('users'))

# Crud teacher
@app.route('/teachers')
def teachers():
    try:
        teachers = ModelTeacher.get_all_teachers(db)  
        return render_template('teachers/teachers.html', teachers=teachers)
    except Exception as ex:
        flash("Ocurrió un error al recuperar los profesores.")
        return redirect(url_for('home'))

@app.route('/create_teacher', methods=['GET', 'POST'])
def create_teacher():
    if request.method == 'POST':        
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        sexo = request.form['sexo']
        ci = request.form['ci']
        num_celular = request.form['num_celular']
        fecha_ingreso = request.form['fecha_ingreso']        
        materias = request.form.getlist('subjects[]')
        
        estado = 'activo'
        id_user = current_user.id 
        
        fecha_ingreso = datetime.datetime.strptime(fecha_ingreso, '%Y-%m-%d')

        # Crear usuario automáticamente
        usuario = ci  # Usar el CI como nombre de usuario
        print(ci)
        password = f"{nombres.split()[0]}_{ci}"  # Crear contraseña como nombre_ci
        print(password)
        hashed_password = generate_password_hash(password)  # Encriptar contraseña
        print(hashed_password)
        nombre_completo = f"{nombres} {apellidos}"
        print(nombre_completo)
        estado="activo"
        print(estado)

        # Insertar el usuario en la tabla `users`
        cursor = db.connection.cursor()
        user_query = """
            INSERT INTO users (usuario, contrasena, nombre_completo, rol, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(user_query, (usuario, hashed_password, nombre_completo, 'docente', estado))
        db.connection.commit()

        teacher = Teacher(0, nombres, apellidos, sexo, ci, num_celular, fecha_ingreso, estado, id_user)
                
        teacher_id = ModelTeacher.create_teacher(db, teacher)
        
        if teacher_id:                                                
            if materias:
                cursor = db.connection.cursor()
                for subject_id in materias:
                    query_subject_teacher = """
                        INSERT INTO subject_teacher (id_teacher, id_subject)
                        VALUES (%s, %s)
                    """
                    cursor.execute(query_subject_teacher, (teacher_id, subject_id))
                db.connection.commit()                
            else:
                print('No se seleccionaron materias.', 'warning')

            return redirect(url_for('teachers'))
        else:
            flash('Error al crear el Docente.', 'danger')
             
    grados = ModelGrade.get_all_grades(db)
    return render_template('teachers/create_teacher.html', grados=grados)




@app.route('/get_subjects_by_grade', methods=['GET'])
def get_subjects_by_grade():
    grade_id = request.args.get('grade_id')
    if not grade_id:
        return jsonify({'error': 'El ID del grado no fue proporcionado.'}), 400

    try:
        subjects = ModelSubject.get_subjects_by_grade(db, grade_id)
        if subjects:
            return jsonify(subjects)
        else:
            return jsonify({'message': 'No se encontraron materias para el grado especificado.'}), 404
    except Exception as ex:
        return jsonify({'error': str(ex)}), 400







@app.route('/edit_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    teacher = ModelTeacher.get_by_id(db, teacher_id)  # Obtener el profesor desde la base de datos
    
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        sexo = request.form['sexo']
        ci = request.form['ci']
        num_celular = request.form['num_celular']
        fecha_ingreso = request.form['fecha_ingreso']
        estado = request.form.get('estado', 'activo')
        id_user = current_user.id         
        fecha_ingreso = datetime.strptime(fecha_ingreso, '%Y-%m-%d')
        
        updated_teacher = Teacher(teacher.id, nombres, apellidos, sexo, ci, num_celular, fecha_ingreso, estado, id_user, teacher.create_at, datetime.now())

        if ModelTeacher.update_teacher(db, updated_teacher):
            flash('Profesor actualizado exitosamente.', 'success')
            return redirect(url_for('teachers'))
        else:
            flash('Error al actualizar el profesor.', 'danger')
            return redirect(url_for('edit_teacher', teacher_id=teacher.id))

    return render_template('teachers/edit_teacher.html', teacher=teacher)



@app.route('/delete_teacher/<int:teacher_id>', methods=['POST'])
def delete_teacher(teacher_id):
    try:
        teacher = ModelTeacher.get_by_id(db, teacher_id)
        if teacher:
            # Primero, eliminar las materias asociadas al docente
            ModelSubjectTeacher.delete_subjects_by_teacher(db, teacher_id)
            
            # Luego, inactivar el docente
            ModelTeacher.delete_teacher(db, teacher_id)
            
            flash("Profesor y sus materias eliminados exitosamente.", 'success')
        else:
            flash("Profesor no encontrado.", 'danger')
    except Exception as ex:
        flash(f"Ocurrió un error: {ex}", 'danger')
    return redirect(url_for('teachers'))



@app.route('/edit_subject_teacher/<int:teacher_id>', methods=['GET', 'POST'])
def edit_subject_teacher(teacher_id):
    teacher = ModelTeacher.get_by_id(db, teacher_id)
    gradoOld = ModelSubjectTeacher.get_teacher_grade(db, teacher_id)  # Obtener el grado asignado
    grado_id = gradoOld[0]

    if request.method == 'POST':
        # Obtener las materias seleccionadas del formulario
        selected_subjects = request.form.getlist('subjects[]')  # Lista de IDs de materias seleccionadas

        # Convertir a enteros por seguridad
        selected_subjects = [int(subject_id) for subject_id in selected_subjects]

        # Borrar materias actuales del docente
        ModelSubjectTeacher.delete_by_teacher(db, teacher_id)

        # Insertar los nuevos registros
        for subject_id in selected_subjects:
            ModelSubjectTeacher.add_subject_to_teacher(db, teacher_id, subject_id)

        flash("Materias actualizadas con éxito", "success")
        return redirect(url_for('teachers'))  # Redirigir a la lista de profesores

    grados = ModelGrade.get_all_grades(db)  # Obtener todos los grados disponibles
    subjects = ModelSubjectTeacher.get_subjects_by_teacher(db, teacher_id)  # Materias actuales

    return render_template(
        'teachers/edit_subject_teacher.html',
        teacher=teacher,
        grados=grados,
        grado_id=grado_id,  # Pasar el grado al template  
        subjects=subjects      
    )


@app.route('/get_subjects_by_grade_and_teacher', methods=['GET'])
def get_subjects_by_grade_and_teacher():
    try:
        grade_id = request.args.get('grade_id', type=int)
        teacher_id = request.args.get('teacher_id', type=int)

        # Depuración: Verificar si los parámetros se recibieron correctamente
        print(f"Grade ID: {grade_id}, Teacher ID: {teacher_id}")
        
        if not grade_id or not teacher_id:
            return jsonify({"error": "Parámetros inválidos"}), 400

        # Lógica para obtener las materias
        subjects = ModelSubjectTeacher.get_subjects_by_grade_and_teacher(db, grade_id, teacher_id)

        # Depuración: Verificar el resultado de la consulta
        print(f"Subjects: {subjects}")

        return jsonify(subjects)
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({"error": "Error al obtener materias"}), 500

# Crud courses - grades
@app.route('/grades')
def grades():
    try:
        grades = ModelGrade.get_all_grades(db)  
        return render_template('courses/grades.html', grades=grades)
    except Exception as ex:
        flash("Ocurrió un error al recuperar los grados.")
        return redirect(url_for('home'))
    
@app.route('/create_grade', methods=['GET', 'POST'])
def create_grade():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ciclo = request.form['ciclo']       
                
        grade = Grade(0, nombre, ciclo)

        if ModelGrade.create_grade(db, grade):
            flash('Grade creado exitosamente.', 'success')
            return redirect(url_for('grades'))
        else:
            flash('Error al crear el Grade.', 'danger')
    
    return render_template('courses/create_grade.html')

@app.route('/edit_grade/<int:grade_id>', methods=['GET', 'POST'])
def edit_grade(grade_id):
    grade = ModelGrade.get_by_id(db, grade_id)  
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        ciclo = request.form['ciclo']
 
        updated_grade = Grade(grade.id, nombre, ciclo)

        if ModelGrade.update_grade(db, updated_grade):
            flash('Grado actualizado exitosamente.', 'success')
            return redirect(url_for('grades'))
        else:
            flash('Error al actualizar el profesor.', 'danger')
            return redirect(url_for('edit_grade', grade_id=grade.id))

    return render_template('courses/edit_grade.html', grade=grade)

@app.route('/delete_grade/<int:grade_id>', methods=['POST'])
def delete_grade(grade_id):
    try:
        grade = ModelGrade.get_by_id(db, grade_id) 
        if grade:            
            ModelGrade.delete_grade(db, grade_id)
            flash("Grado eliminado exitosamente.", 'success')
        else:
            flash("Grado no encontrado.", 'danger')
    except Exception as ex:
        flash(f"Ocurrió un error: {ex}", 'danger')
    return redirect(url_for('grades'))

# Crud courses - sections
@app.route('/sections')
def sections():
    try:
        sections = ModelSection.get_all_sections(db)  
        return render_template('courses/sections.html', sections=sections)
    except Exception as ex:
        flash("Ocurrió un error al recuperar los secciones.")
        return redirect(url_for('home'))
    
@app.route('/create_section', methods=['GET', 'POST'])
def create_section():
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_grado = request.form['id_grado']       
                
        section = Section(0, nombre, id_grado)

        if ModelSection.create_section(db, section):
            flash('Seccion creado exitosamente.', 'success')
            return redirect(url_for('sections'))
        else:
            flash('Error al crear el Grade.', 'danger')

    grados = ModelGrade.get_all_grades(db)
    return render_template('courses/create_section.html', grados=grados)

@app.route('/edit_section/<int:section_id>', methods=['GET', 'POST'])
def edit_section(section_id):
    section = ModelSection.get_by_id(db, section_id)      
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_grado = request.form['id_grado']
 
        updated_section = Section(section.id, nombre, id_grado)

        if ModelSection.update_section(db, updated_section):
            flash('Seccion actualizado exitosamente.', 'success')
            return redirect(url_for('sections'))
        else:
            flash('Error al actualizar el Seccion.', 'danger')
            return redirect(url_for('edit_section', section_id=section.id))

    grados = ModelGrade.get_all_grades(db)
    return render_template('courses/edit_section.html', section=section, grados=grados)

@app.route('/delete_section/<int:section_id>', methods=['POST'])
def delete_section(section_id):
    try:
        section = ModelSection.get_by_id(db, section_id) 
        if section:            
            ModelSection.delete_section(db, section_id)
            flash("Seccion eliminado exitosamente.", 'success')
        else:
            flash("Seccion no encontrado.", 'danger')
    except Exception as ex:
        flash(f"Ocurrió un error: {ex}", 'danger')
    return redirect(url_for('sections'))

# Crud courses - subjects
@app.route('/subjects')
def subjects():
    try:
        subjects = ModelSubject.get_all_subjects(db)  
        return render_template('courses/subjects.html', subjects=subjects)
    except Exception as ex:
        flash("Ocurrió un error al recuperar los secciones.")
        return redirect(url_for('home'))

@app.route('/create_subject', methods=['GET', 'POST'])
def create_subject():
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_grado = request.form['id_grado']       
                
        subject = Subject(0, nombre, id_grado)

        if ModelSubject.create_subject(db, subject):
            flash('Materia creado exitosamente.', 'success')
            return redirect(url_for('subjects'))
        else:
            flash('Error al crear el Materia.', 'danger')

    grados = ModelGrade.get_all_grades(db)
    return render_template('courses/create_subject.html', grados=grados)

@app.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    subject = ModelSubject.get_by_id(db, subject_id)      
    if request.method == 'POST':
        nombre = request.form['nombre']
        id_grado = request.form['id_grado']
 
        update_subject = Subject(subject.id, nombre, id_grado)

        if ModelSubject.update_subject(db, update_subject):
            flash('Materia actualizado exitosamente.', 'success')
            return redirect(url_for('subjects'))
        else:
            flash('Error al actualizar el Materia.', 'danger')
            return redirect(url_for('edit_subject', subject_id=subject.id))

    grados = ModelGrade.get_all_grades(db)
    return render_template('courses/edit_subject.html', subject=subject, grados=grados)

@app.route('/delete_subject/<int:subject_id>', methods=['POST'])
def delete_subject(subject_id):
    try:
        subject = ModelSubject.get_by_id(db, subject_id) 
        if subject:            
            ModelSubject.delete_subject(db, subject_id)
            flash("Materia eliminado exitosamente.", 'success')
        else:
            flash("Materia no encontrado.", 'danger')
    except Exception as ex:
        flash(f"Ocurrió un error: {ex}", 'danger')
    return redirect(url_for('subjects'))

# Crud Students
@app.route('/students')
def students():
    try:
        students = ModelStudent.get_all_students(db)  
        return render_template('students/students.html', students=students)
    except Exception as ex:
        flash("Ocurrió un error al recuperar Estudiantes.")
        return redirect(url_for('home'))
    
# Listar estudiantes segun el docente
@app.route('/students_teacher')
def students_teacher():
    try:
        # Obtener el CI del docente logeado
        ci = current_user.usuario  # Suponiendo que el 'usuario' contiene el CI del docente
        print(ci)
        # Obtener el teacher_id usando el CI
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT id FROM teachers WHERE ci = %s
        """, (ci,))
        teacher = cursor.fetchone()

        if not teacher:
            flash("No se encontró al docente asociado.", 'warning')
            return redirect(url_for('home'))  # Redirigir a la página principal si no se encuentra el docente

        teacher_id = teacher[0]  # El ID del docente
        print(teacher_id)
        # Obtener los estudiantes asociados al docente
        cursor.execute("""
            SELECT 
                sn.id,
                s.nombres AS nombre_estudiante,
                s.apellidos as apellidos,
                s.ci as ci,
                s.genero,
                s.num_celular,
                s.fecha_nacimiento,
                s.fecha_ingreso,
                CONCAT(g.nombre, ' - ', g.ciclo) AS grado,
                sec.nombre AS seccion,
                sub.nombre AS materia
                
            FROM 
                stundent_notes sn
            JOIN inscriptions i ON sn.id_inscription = i.id
            JOIN students s ON i.id_student = s.id
            JOIN grados g ON i.id_grado = g.id
            JOIN sections sec ON i.id_section = sec.id
            JOIN subjects sub ON sn.id_subject = sub.id
            JOIN subject_teacher st ON st.id_subject = sub.id
            WHERE st.id_teacher = %s AND i.año_escolar = 2024
            ORDER BY s.nombres, g.nombre, sec.nombre, sub.nombre
        """, (teacher_id,))  # Filtramos por el ID del docente

        students = cursor.fetchall()

        if not students:
            flash("No se encontraron estudiantes asociados a este docente.", 'warning')

        return render_template('students/students_teacher.html', students=students)

    except Exception as ex:
        flash("Ocurrió un error al recuperar los estudiantes.", 'danger')
        return redirect(url_for('home'))
    finally:
        cursor.close()

# Reportes por materia del docente
@app.route('/get_subjects')
def get_subjects():
    try:
        ci = current_user.usuario  # CI del docente logeado
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT id FROM teachers WHERE ci = %s
        """, (ci,))
        teacher = cursor.fetchone()

        if not teacher:
            return jsonify({"error": "No se encontró al docente asociado."}), 404

        teacher_id = teacher[0]
        cursor.execute("""
            SELECT sub.id, sub.nombre
            FROM subject_teacher st
            JOIN subjects sub ON st.id_subject = sub.id
            WHERE st.id_teacher = %s
        """, (teacher_id,))
        subjects = cursor.fetchall()

        return jsonify(subjects)  # Retorna las materias en formato JSON
    except Exception as ex:
        return jsonify({"error": "Ocurrió un error al recuperar las materias."}), 500
    finally:
        cursor.close()

@app.route('/get_students/<int:subject_id>')
def get_students(subject_id):
    try:
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT 
                s.nombres, 
                s.apellidos, 
                s.ci, 
                CONCAT(g.nombre, ' - ', g.ciclo) AS grado,
                sec.nombre AS seccion,
                sub.nombre AS materia
            FROM 
                stundent_notes sn
            JOIN inscriptions i ON sn.id_inscription = i.id
            JOIN students s ON i.id_student = s.id
            JOIN grados g ON i.id_grado = g.id
            JOIN sections sec ON i.id_section = sec.id
            JOIN subjects sub ON sn.id_subject = sub.id
            WHERE 
                sn.id_subject = %s 
                AND i.año_escolar = 2024
            ORDER BY 
                s.nombres;
        """, (subject_id,))
        students = cursor.fetchall()

        return jsonify(students)  # Retorna los estudiantes en formato JSON
    except Exception as ex:
        return jsonify({"error": "Ocurrió un error al recuperar los estudiantes."}), 500
    finally:
        cursor.close()







@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']       
        ci = request.form['ci']       
        genero = request.form['genero']       
        num_celular = request.form['num_celular']       
        fecha_nacimiento = request.form['fecha_nacimiento']               
        fecha_ingreso = request.form['fecha_ingreso']                      

        estado = 'activo'
        id_user = current_user.id 
        
        fecha_ingreso = datetime.datetime.strptime(fecha_ingreso, '%Y-%m-%d')

        student = Student(0, nombres, apellidos, ci, genero, num_celular, fecha_nacimiento, estado, fecha_ingreso, id_user)

        if ModelStudent.create_student(db, student):
            flash('Estudiante creado exitosamente.', 'success')
            return redirect(url_for('students'))
        else:
            flash('Error al crear el Estudiante.', 'danger')
    
    return render_template('students/create_student.html')

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = ModelStudent.get_by_id(db, student_id)      
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']       
        ci = request.form['ci']       
        genero = request.form['genero']       
        num_celular = request.form['num_celular']       
        fecha_nacimiento = request.form['fecha_nacimiento']                               
        fecha_ingreso = request.form.get('fecha_ingreso', student.fecha_ingreso)  # Usa la existente si no se actualiza
        estado = request.form.get('estado', student.estado)  # Usa el estado actual si no se cambia
        id_user = current_user.id         

        update_student = Student(student.id, nombres, apellidos, ci, genero, num_celular, fecha_nacimiento, estado, fecha_ingreso, id_user)

        if ModelStudent.update_student(db, update_student):
            flash('Estudiante actualizado exitosamente.', 'success')
            return redirect(url_for('students'))
        else:
            flash('Error al actualizar el Estudiante.', 'danger')
            return redirect(url_for('edit_student', student_id=student.id))
    
    return render_template('students/edit_student.html', student=student)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        student = ModelStudent.get_by_id(db, student_id) 
        if student:            
            ModelStudent.delete_student(db, student_id)
            flash("Estudiante eliminado exitosamente.", 'success')
        else:
            flash("Estudiante no encontrado.", 'danger')
    except Exception as ex:
        flash(f"Ocurrió un error: {ex}", 'danger')
    return redirect(url_for('students'))

# Crud Listar inscripciones
@app.route('/inscriptions')
def inscriptions():
    try:
        cursor = db.connection.cursor()

        cursor.execute("Select * from inscriptions")
        inscriptions = cursor.fetchall()
        return render_template('inscriptions/inscriptions.html', inscriptions=inscriptions)
    except Exception as ex:
        flash("Ocurrió un error al recuperar Estudiantes.")
        return redirect(url_for('home'))


# Crear inscripciones
@app.route('/create_inscriptions', methods=['GET', 'POST'])
def create_inscriptions():
    if request.method == 'POST':
        # Obtener los datos del formulario
        ci = request.form.get('ci')
        id_grado = request.form['id_grado']
        id_section = request.form['id_section']        
        nombre_tutor = request.form['nombre_tutor']
        celular_tutor = request.form['celular_tutor']
        direccion_estudiante = request.form['direccion_estudiante']
        gestion = datetime.datetime.now().year  # O usar un valor dinámico para el año escolar
        print(gestion)

        try:
            cursor = db.connection.cursor()

            # Buscar al estudiante por CI
            cursor.execute("SELECT id FROM students WHERE ci = %s", (ci,))
            student = cursor.fetchone()

            if student:
                id_student = student[0]
                ## print(id_student)

                # Verificar si el estudiante ya está inscrito en la gestión 2024
                cursor.execute("""
                    SELECT COUNT(*) FROM inscriptions 
                    WHERE id_student = %s AND año_escolar = %s
                """, (id_student, gestion))
                existing_inscriptions = cursor.fetchone()[0]

                if existing_inscriptions > 0:
                    flash('El estudiante ya está inscrito en este año escolar.', 'warning')
                    print('El estudiante ya está inscrito en este año escolar.')
                else:
                    # Insertar nueva inscripción
                    sql = """
                        INSERT INTO inscriptions 
                        (id_student, id_grado, id_section, nombre_tutor, celular_tutor, direccion_estudiante, estado, año_escolar, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, 'activo', %s, NOW(), NOW())
                    """
                    values = (id_student, id_grado, id_section, nombre_tutor, celular_tutor, direccion_estudiante, gestion)
                    cursor.execute(sql, values)
                    db.connection.commit()

                    # Obtener el id_inscription de la inscripción recién insertada
                    cursor.execute("SELECT LAST_INSERT_ID()")
                    id_inscription = cursor.fetchone()[0]
                    print(f"ID de inscripción (fijo): {id_inscription}")

                    # Obtener las materias del grado
                    cursor.execute("SELECT id FROM subjects WHERE id_grado = %s", (id_grado,))
                    subjects = cursor.fetchall()
                    ## print(subjects)
                    # Insertar notas para cada materia
                    for subject in subjects:
                        id_subject = subject[0]
                        print("primer ",id_subject)
                        # Insertar cada materia en la tabla de notas
                       
                        # Insertar cada materia en la tabla de notas
                        insert_notes_sql = """
                            INSERT INTO stundent_notes 
                            (id_inscription, id_subject, nota1, nota2, nota3, nota4, promedio, observaciones, created_at, updated_at)
                            VALUES (%s, %s, 0.00, 0.00, 0.00, 0.00, 0.00, '', NOW(), NOW())
                        """
                        cursor.execute(insert_notes_sql, (id_inscription, id_subject))
                    db.connection.commit()

                    flash('Estudiante inscrito exitosamente.', 'success')
                    print('Estudiante inscrito exitosamente.')
            else:
                flash('Estudiante no encontrado. Verifique el CI.', 'danger')

        except Exception as e:
            # Manejo de errores
            db.connection.rollback()
            flash(f'Error al inscribir al estudiante: {str(e)}', 'danger')

        finally:
            cursor.close()

        # Redireccionar al formulario para nuevas inscripciones
        return redirect(url_for('inscriptions'))
    
    grados = ModelGrade.get_all_grades(db)
    # Renderizar el formulario en el método GET
    return render_template('inscriptions/create_inscriptions.html', grados=grados)



@app.route('/buscar-estudiante')
def buscar_estudiante():
    ci = request.args.get('ci')
    cursor = db.connection.cursor()
    cursor.execute("SELECT nombres, apellidos FROM students WHERE ci = %s and estado = 'activo'", (ci,) )
    student = cursor.fetchone()
    cursor.close()

    if student:
        return jsonify({'encontrado': True, 'nombres': student[0], 'apellidos': student[1]})
    else:
        return jsonify({'encontrado': False})

@app.route('/get_sections/<int:grado_id>', methods=['GET'])
def get_sections(grado_id):
    try:
        cursor = db.connection.cursor()
        # Obtener las secciones relacionadas con el grado
        cursor.execute("SELECT id, nombre FROM sections WHERE id_grado = %s", (grado_id,))
        sections = cursor.fetchall()
        cursor.close()

        # Convertir los resultados a un formato JSON
        sections_list = [{'id': section[0], 'nombre': section[1]} for section in sections]
        return jsonify(sections_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Listar Notas de los estudiantes
@app.route('/notes')
def notes():
    try:
        cursor = db.connection.cursor()
        
        # Ejecutar la consulta SQL para obtener los datos
        cursor.execute("""
            SELECT 
                sn.id,
                s.nombres AS nombre_estudiante,
                CONCAT(g.nombre, ' - ', g.ciclo) AS grado,
                sec.nombre AS seccion,
                sub.nombre AS materia,
                sn.nota1, 
                sn.nota2, 
                sn.nota3, 
                sn.nota4, 
                sn.promedio, 
                sn.observaciones
            FROM 
                stundent_notes sn
            JOIN inscriptions i ON sn.id_inscription = i.id
            JOIN students s ON i.id_student = s.id
            JOIN grados g ON i.id_grado = g.id
            JOIN sections sec ON i.id_section = sec.id
            JOIN subjects sub ON sn.id_subject = sub.id
            WHERE i.año_escolar = %s
            ORDER BY s.nombres, g.nombre, sec.nombre, sub.nombre
        """, (2024,))  # Puedes poner el año escolar dinámicamente si lo deseas

        # Obtener todos los resultados
        notes = cursor.fetchall()

        # Si no hay resultados
        if not notes:
            flash("No se encontraron notas para este año escolar.", 'warning')

        return render_template('notes/student_notes.html', notes=notes)

    except Exception as e:
        flash(f"Error al listar las notas: {str(e)}", 'danger')

    finally:
        cursor.close()

# notas para docente
@app.route('/notes_teacher')
def notes_teacher():
    try:
        if current_user.rol != 'docente':
            flash("No tienes permisos para acceder a esta sección.", 'danger')
            return redirect(url_for('docente_home.html'))

        # Obtener el ID del docente actual
        ci = current_user.usuario
        print(ci)
        cursor = db.connection.cursor()
        cursor.execute("""
            SELECT id FROM teachers WHERE ci = %s
        """, (ci,))
        teacher = cursor.fetchone()

        if not teacher:
            flash("No se encontró al docente asociado.", 'warning')
            return redirect(url_for('docente_home.html'))

        teacher_id = teacher[0]
        print(teacher_id)

        # Consulta para listar estudiantes de las materias del docente
        cursor.execute("""
            SELECT 
                sn.id,
                s.nombres AS nombre_estudiante,
                CONCAT(g.nombre, ' - ', g.ciclo) AS grado,
                sec.nombre AS seccion,
                sub.nombre AS materia,
                sn.nota1, 
                sn.nota2, 
                sn.nota3, 
                sn.nota4, 
                sn.promedio, 
                sn.observaciones
            FROM 
                stundent_notes sn
            JOIN inscriptions i ON sn.id_inscription = i.id
            JOIN students s ON i.id_student = s.id
            JOIN grados g ON i.id_grado = g.id
            JOIN sections sec ON i.id_section = sec.id
            JOIN subjects sub ON sn.id_subject = sub.id
            JOIN subject_teacher st ON st.id_subject = sub.id
            WHERE st.id_teacher = %s AND i.año_escolar = %s
            ORDER BY s.nombres, g.nombre, sec.nombre, sub.nombre
        """, (teacher_id, 2024))  # Año escolar puede ser dinámico

        # Obtener todos los resultados
        notes = cursor.fetchall()

        # Si no hay resultados
        if not notes:
            flash("No se encontraron notas para este año escolar.", 'warning')
        
        print(notes)
        return render_template('notes/teacher_notes.html', notes=notes)

    except Exception as e:
        flash(f"Error al listar las notas: {str(e)}", 'danger')

    finally:
        cursor.close()


@app.route('/edit_student_note/<int:id>', methods=['GET', 'POST'])
def edit_student_note(id):
    try:
        cursor = db.connection.cursor()
        
        # Obtener la nota específica para editar
        cursor.execute("""
            SELECT sn.id, s.nombres AS estudiante, sub.nombre AS materia, 
                   sn.nota1, sn.nota2, sn.nota3, sn.nota4, sn.observaciones 
            FROM stundent_notes sn
            JOIN inscriptions i ON sn.id_inscription = i.id
            JOIN students s ON i.id_student = s.id
            JOIN subjects sub ON sn.id_subject = sub.id
            WHERE sn.id = %s
        """, (id,))
        student_note = cursor.fetchone()
        
        if request.method == 'POST':
            # Obtener datos actualizados del formulario
            nota1 = request.form['nota1']
            nota2 = request.form['nota2']
            nota3 = request.form['nota3']
            nota4 = request.form['nota4']
            observaciones = request.form['observaciones']

            # Actualizar los datos en la base de datos
            update_sql = """
                UPDATE stundent_notes 
                SET nota1 = %s, nota2 = %s, nota3 = %s, nota4 = %s, observaciones = %s, updated_at = NOW()
                WHERE id = %s
            """
            cursor.execute(update_sql, (nota1, nota2, nota3, nota4, observaciones, id))
            db.connection.commit()
            flash('Notas actualizadas con éxito.', 'success')
            # Verificar el rol del usuario
            if current_user.rol == 'docente':
                # Redirigir a las notas del docente
                return redirect(url_for('notes_teacher'))  # Cambia esto si la ruta del docente es diferente
            else:
                # Redirigir a las notas del administrador o vista general
                return redirect(url_for('notes'))  # Ruta donde se muestran las notas de todos

        return render_template('notes/edit_student_note.html', student_note=student_note)
    except Exception as e:
        db.connection.rollback()
        flash(f'Error al actualizar las notas: {str(e)}', 'danger')
    finally:
        cursor.close()





# Reportes
@app.route('/report_users')
def report_users():    
    users = ModelUser.get_all_users(db)    
    return render_template('users/report_users.html', users=users)

# Reportes de notas de un estudiante
@app.route('/report_students')
def report_students():    
    try:
        students = ModelStudent.get_all_students(db)  
        return render_template('reports/students.html', students=students, user_role=current_user.rol)
    except Exception as ex:
        flash("Ocurrió un error al recuperar Estudiantes.")
        return redirect(url_for('home'))

@app.route('/generate_pdf/<int:student_id>')
def generate_pdf(student_id):
    # Obtener información del estudiante y sus notas
    cursor = db.connection.cursor()
    cursor.execute("""
        SELECT CONCAT(s.nombres,' ',s.apellidos) as nombres, CONCAT(g.nombre, ' - ', g.ciclo) AS grado, concat('Paralelo "', sec.nombre, '"') AS seccion
        FROM students s
        JOIN inscriptions i ON s.id = i.id_student
        JOIN grados g ON i.id_grado = g.id
        JOIN sections sec ON i.id_section = sec.id
        WHERE s.id = %s
    """, (student_id,))
    student_info = cursor.fetchone()

    cursor.execute("""
        SELECT sub.nombre AS materia, sn.nota1, sn.nota2, sn.nota3, sn.nota4,
               ROUND((sn.nota1 + sn.nota2 + sn.nota3 + sn.nota4)/4, 2) AS promedio
        FROM stundent_notes sn
        JOIN subjects sub ON sn.id_subject = sub.id
        WHERE sn.id_inscription = (
            SELECT id FROM inscriptions WHERE id_student = %s
        )
    """, (student_id,))
    student_notes = cursor.fetchall()
    cursor.close()

    # Crear PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter    

    # Título
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(200, height - 50, "Reporte Académico")

    # Información del estudiante
    pdf.setFont("Helvetica", 12)
    y_position = height - 150
    pdf.drawString(50, y_position, f"Nombre del Estudiante: {student_info[0]}")
    pdf.drawString(50, y_position - 20, f"Grado: {student_info[1]}")
    pdf.drawString(50, y_position - 40, f"Sección: {student_info[2]}")

    # Encabezado de tabla
    y_position -= 80
    table_data = [["Materia", "Nota 1", "Nota 2", "Nota 3", "Nota 4", "Promedio"]]
    for note in student_notes:
        table_data.append([note[0], note[1], note[2], note[3], note[4], note[5]])

    # Crear tabla
    table = Table(table_data, colWidths=[120, 50, 50, 50, 50, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))

    # Dibujar tabla en el PDF
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 50, y_position - len(table_data) * 20 - 10)

    # Finalizar PDF
    pdf.save()
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"reporte_estudiante_{student_info[0]}.pdf",
        mimetype='application/pdf'
    )


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()