from werkzeug.security import generate_password_hash

# Cadena a encriptar
password = "password"

# Encriptar la contraseña
encrypted_password = generate_password_hash(password)

# Imprimir la contraseña encriptada
print(encrypted_password)
