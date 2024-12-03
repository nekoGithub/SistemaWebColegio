from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime

from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelTeacher import ModelTeacher
from models.ModelGrade import ModelGrade
from models.ModelSection import ModelSection
from models.ModelSubject import ModelSubject

# Entities:
from models.entities.User import User
from models.entities.Teacher import Teacher
from models.entities.Grade import Grade
from models.entities.Section import Section
from models.entities.Subject import Subject

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
            return redirect(url_for('home'))
        else:
            flash("Usuario o contraseña incorrectos.")
            return render_template('auth/login.html')  
    return render_template('auth/login.html')  



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')

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
        estado = request.form.get('estado', 'activo')  
        id_user = current_user.id 
                
        fecha_ingreso = datetime.strptime(fecha_ingreso, '%Y-%m-%d')
                
        teacher = Teacher(0, nombres, apellidos, sexo, ci, num_celular, fecha_ingreso, estado, id_user)

        if ModelTeacher.create_teacher(db, teacher):
            flash('Profesor creado exitosamente.', 'success')
            return redirect(url_for('teachers'))
        else:
            flash('Error al crear el profesor.', 'danger')
    
    return render_template('teachers/create_teacher.html')

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
            ModelTeacher.delete_teacher(db, teacher_id)
            flash("Profesor eliminado exitosamente.", 'success')
        else:
            flash("Profesor no encontrado.", 'danger')
    except Exception as ex:
        flash(f"Ocurrió un error: {ex}", 'danger')
    return redirect(url_for('teachers'))

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

# Reportes
@app.route('/report_users')
def report_users():    
    users = ModelUser.get_all_users(db)    
    return render_template('users/report_users.html', users=users)

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