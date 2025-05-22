from flask import Flask, jsonify, redirect, request, url_for
import os
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración MySQL
app.config["MYSQL_USER"] = os.getenv("user")
app.config["MYSQL_PASSWORD"] = os.getenv("password")
app.config["MYSQL_HOST"] = os.getenv("host")
app.config["MYSQL_DB"] = os.getenv("db")
app.secret_key = os.getenv("secret_key")

mysql = MySQL(app)

# Habilitar CORS 
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

######################### HOME ########################################
@app.route("/", methods=["GET"])
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, stock, imagen FROM productos ORDER BY CAST(stock AS UNSIGNED) DESC LIMIT 5")
    productos = cursor.fetchall()

    productos_formateados = [
        {
            "id": p[0],
            "nombre": p[1],
            "descripcion": p[2],
            "precio": p[3],
            "stock": p[4],
            "imagen": p[5]
        }
        for p in productos
    ]



    return jsonify({
        "noticia": "¡Bienvenidos a nuestra tienda online artesanal!",
        "destacados": productos_formateados
    })



######################### LOGIN ########################################

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    if user and check_password_hash(user[2], password):
        return jsonify({"message": "Login successful", "user_id": user[0]}), 200
    return jsonify({"error": "Invalid credentials"}), 401

######################### REGISTER ########################################

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son necesarias"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"error": "Email ya en uso"}), 409

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
    mysql.connection.commit()

    return jsonify({"message": "Usuario registrado correctamente"}), 201

######################### PRODUCTOS ########################################
@app.route("/productos", methods=["GET"])
def obtener_productos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, stock, imagen FROM productos ORDER BY CAST(stock AS UNSIGNED) DESC LIMIT 5")
    productos = cursor.fetchall()

    productos_formateados = [
    {
        "id": p[0],
        "nombre": p[1],
        "descripcion": p[2],
        "precio": p[3],
        "stock": p[4],
        "imagen": p[5] 
    }
    for p in productos
]


    return jsonify(productos_formateados)

######################### ADMIN - AÑADIR PRODUCTO ########################################

@app.route('/admin', methods=['POST'])
def add_product():
    print("POST /admin recibido")
    print("Datos recibidos:", request.json)  # <-- LOG PARA VER LOS DATOS
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    stock = data.get('stock')
    imagen = data.get('imagen')

    # Validar todos los campos obligatorios
    if not nombre or not descripcion or precio is None or stock is None or not imagen:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    try:
        precio = float(precio)
        stock = int(stock)
    except (ValueError, TypeError):
        return jsonify({'error': 'Precio o stock inválidos'}), 400

    cursor = mysql.connection.cursor()

    try:
        sql = "INSERT INTO productos (nombre, descripcion, precio, stock, imagen) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, descripcion, precio, stock, imagen))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        print("ERROR AL AÑADIR PRODUCTO:", e)
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'error': 'Error al añadir producto: ' + str(e)}), 500


    return jsonify({'message': 'Producto añadido correctamente'}), 201

######################### ADMIN - ELIMINAR PRODUCTO ########################################
@app.route('/admin/<int:producto_id>', methods=['DELETE'])
def delete_product(producto_id):
    print(f"DELETE /admin/{producto_id} recibido")
    cursor = mysql.connection.cursor()

    try:
        sql = "DELETE FROM productos WHERE id = %s"
        cursor.execute(sql, (producto_id,))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        print("ERROR AL ELIMINAR PRODUCTO:", e)
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'error': 'Error al eliminar producto: ' + str(e)}), 500

    return jsonify({'message': 'Producto eliminado correctamente'}), 200

######################### ADMIN - EDITAR PRODUCTO ########################################

# Obtener datos de un producto por ID (solo para admins)
@app.route('/admin/editar/<int:producto_id>', methods=['GET'])
def get_producto_admin(producto_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, stock, imagen FROM productos WHERE id = %s", (producto_id,))
    p = cursor.fetchone()
    cursor.close()
    if p:
        producto = {
            "id": p[0],
            "nombre": p[1],
            "descripcion": p[2],
            "precio": p[3],
            "stock": p[4],
            "imagen": p[5]
        }
        return jsonify(producto)
    return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/admin/<int:producto_id>', methods=['PUT'])
def actualizar_producto_admin(producto_id):
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    stock = data.get('stock')
    imagen = data.get('imagen')

    if not nombre or not descripcion or precio is None or stock is None or not imagen:
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, imagen=%s
            WHERE id=%s
        """, (nombre, descripcion, precio, stock, imagen, producto_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Producto actualizado correctamente'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500



######################### TIENDA ########################################

@app.route('/tienda', methods=['GET'])
def tienda():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, stock, imagen FROM productos ORDER BY id DESC")
    productos = cursor.fetchall()
    cursor.close()

    productos_formateados = [
        {
            "id": p[0],
            "nombre": p[1],
            "descripcion": p[2],
            "precio": p[3],
            "stock": p[4],
            "imagen": p[5]
        }
        for p in productos
    ]

    return jsonify(productos_formateados)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
