import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "usuarios.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Insertar integrantes de prueba con contraseñas seguras (Hash)
    integrantes = [
        ("Christian_Faundez", "Duoc.1234"),
        ("Bastian_Gomez", "Duoc.1234"), 
    ]
    
    for nom, psw in integrantes:
        hashed = generate_password_hash(psw) 
        try:
            cursor.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (nom, hashed))
        except sqlite3.IntegrityError:
            pass # Ya existen en la base de datos
            
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (usuario,))
    row = cursor.fetchone()
    conn.close()
    
    if row and check_password_hash(row[0], password):
        return jsonify({"status": "success", "message": f"Bienvenido/a {usuario}!"}), 200
    return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

if __name__ == "__main__":
    init_db()
    print("Base de datos SQLite lista para visualizar en DB Browser.") 
    app.run(host="0.0.0.0", port=5800, debug=True) 