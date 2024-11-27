from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

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
        
        print(f"Datos recibidos: {usuario}, {contrasena}, {nombre_completo}")
        
        user = User(0, usuario, contrasena, nombre_completo=nombre_completo)
        
        if ModelUser.create_user(db, user):
            #flash('Usuario creado exitosamente.', 'success')
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
                
        if contrasena:
            contrasena_encriptada = generate_password_hash(contrasena)
        else:            
            contrasena_encriptada = user.contrasena          
        
        updated_user = User(user.id, usuario, contrasena_encriptada, nombre_completo)
                
        if ModelUser.update_user(db, updated_user):
            #flash('Usuario actualizado exitosamente.', 'success')
            return redirect(url_for('users'))
        else:
            flash('Error al actualizar el usuario.', 'danger')
            return redirect(url_for('edit_user', user_id=user.id))

    return render_template('users/edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        user = ModelUser.get_by_id(db, user_id)  # Obtener el usuario por ID
        if user:
            # Eliminar el usuario de la base de datos
            ModelUser.delete_user(db, user_id)
            flash("Usuario eliminado exitosamente.", 'success')
        else:
            flash("Usuario no encontrado.", 'danger')
    except Exception as ex:
        flash(f"Ocurrió un error: {ex}", 'danger')
    return redirect(url_for('users'))

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