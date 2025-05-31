from flask import Flask, jsonify, request
import os
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import smtplib
from email.message import EmailMessage

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  

# Configuración MySQL
app.config["MYSQL_USER"] = os.getenv("user")
app.config["MYSQL_PASSWORD"] = os.getenv("password")
app.config["MYSQL_HOST"] = os.getenv("host")
app.config["MYSQL_DB"] = os.getenv("db")
mysql = MySQL(app)

# Configurar CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

# Modelo de usuario para Flask-Login
class User(UserMixin):
    def __init__(self, id_, email):
        self.id = id_
        self.email = email
    
    def is_admin(self):
        return self.email == "admin@example.com"

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user[0], user[1])
    return None

@app.route("/auth/user", methods=["GET"])
@login_required
def get_authenticated_user():
    return jsonify({
        "id": current_user.id,
        "email": current_user.email
    })


@app.route("/", methods=["GET"])
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, stock, imagen FROM productos ORDER BY CAST(stock AS UNSIGNED) DESC LIMIT 5")
    productos = cursor.fetchall()
    cursor.close()

    productos_formateados = [
        {
            "id": p[0],
            "nombre": p[1],
            "descripcion": p[2],
            "precio": float(p[3]),
            "stock": int(p[4]),
            "imagen": p[5]
        }
        for p in productos
    ]

    return jsonify({
        "noticia": "¡Bienvenidos a nuestra tienda online!",
        "destacados": productos_formateados
    })

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":

        return jsonify({"message": "Por favor, inicia sesión usando POST"}), 200
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, email, password FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user[2], password):
        user_obj = User(user[0], user[1])
        login_user(user_obj) 
        return jsonify({"message": "Login exitoso", "user_id": user[0], "email": user[1]}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Sesión cerrada correctamente"}), 200

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son necesarias"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        return jsonify({"error": "Email ya en uso"}), 409

    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Usuario registrado correctamente"}), 201

@app.route("/productos", methods=["GET"])
def obtener_productos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, descripcion, precio, stock, imagen FROM productos ORDER BY CAST(stock AS UNSIGNED) DESC")
    productos = cursor.fetchall()
    cursor.close()

    productos_formateados = [
        {
            "id": p[0],
            "nombre": p[1],
            "descripcion": p[2],
            "precio": float(p[3]),
            "stock": int(p[4]),
            "imagen": p[5]
        }
        for p in productos
    ]

    return jsonify(productos_formateados)


@app.route('/admin', methods=['POST'])
def add_product():
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    stock = data.get('stock')
    imagen = data.get('imagen')

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
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'error': 'Error al añadir producto: ' + str(e)}), 500

    return jsonify({'message': 'Producto añadido correctamente'}), 201

@app.route('/admin/<int:producto_id>', methods=['DELETE'])
def delete_product(producto_id):
    cursor = mysql.connection.cursor()

    try:
        sql = "DELETE FROM productos WHERE id = %s"
        cursor.execute(sql, (producto_id,))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'error': 'Error al eliminar producto: ' + str(e)}), 500

    return jsonify({'message': 'Producto eliminado correctamente'}), 200

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
            "precio": float(p[3]),
            "stock": int(p[4]),
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
        precio = float(precio)
        stock = int(stock)
    except (ValueError, TypeError):
        return jsonify({'error': 'Precio o stock inválidos'}), 400

    cursor = mysql.connection.cursor()

    try:
        cursor.execute("""
            UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, imagen=%s
            WHERE id=%s
        """, (nombre, descripcion, precio, stock, imagen, producto_id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Producto actualizado correctamente'})
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return jsonify({'error': str(e)}), 500

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
            "precio": float(p[3]),
            "stock": int(p[4]),
            "imagen": p[5]
        }
        for p in productos
    ]

    return jsonify(productos_formateados)

@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return jsonify({
        "mensaje": "Aquí iría la lógica del carrito si se guardara en el backend"
    })

@app.route("/pago", methods=["POST"])
def procesar_pago():
    data = request.get_json()

    email_comprador = data.get("email")
    carrito = data.get("carrito")
    total = data.get("total")
    direccion = data.get("direccion")
    ciudad = data.get("ciudad")
    cp = data.get("cp")
    provincia = data.get("provincia")

    if not all([email_comprador, carrito, total is not None, direccion, ciudad, cp, provincia]):
        return jsonify({"error": "Faltan datos necesarios para procesar el pago"}), 400

    productos = "\n".join(
        [f"{item['nombre']} x {item['cantidad']} - {item['precio']}€ c/u" for item in carrito]
    )

    mensaje = (
        f"Mensaje:\n"
        f"Gracias por tu compra, esperemos que te guste mucho!.\n\n Aquí tienes el resumen de tu pedido:\n"
        f"{productos}\n\n"
        f"Total: {total}€\n\n"
        f"Dirección de envío:\n{direccion}\n{cp}, {ciudad}, {provincia}\n\n"
        f"Nos pondremos en contacto contigo si hay novedades.\n"
    )

    try:
        email_message = EmailMessage()
        email_message["Subject"] = "Confirmación de compra"
        email_message["From"] = os.getenv("EMAIL_SENDER")
        email_message["To"] = email_comprador
        email_message.set_content(mensaje)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(email_message)

    except Exception as e:
        print("Error al enviar el correo:", e)
        return jsonify({"error": "Error al enviar el correo de confirmación"}), 500
    

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            INSERT INTO pagos (email, productos, total, direccion, ciudad, cp, provincia)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (email_comprador, productos, total, direccion, ciudad, cp, provincia)
        )
        mysql.connection.commit()
    except Exception as e:
        print("Error al guardar en la base de datos:", e)
        return jsonify({"error": "Error al guardar el pago"}), 500
    finally:
        cursor.close()
        return jsonify({"message": "Pago procesado y correo enviado"}), 200

@app.route("/contacto", methods=["POST"])
def enviar_contacto():
    data = request.get_json()

    nombre = data.get("nombre")
    email = data.get("email")
    mensaje = data.get("mensaje")

    if not nombre or not email or not mensaje:
        return jsonify({"error": "Faltan campos"}), 400

    email_message = EmailMessage()
    email_message["Subject"] = "Nuevo mensaje desde formulario de contacto"
    email_message["From"] = os.getenv("EMAIL_SENDER")
    email_message["To"] = os.getenv("EMAIL_RECEIVER")
    email_message.set_content(
        f"Nombre: {nombre}\nCorreo: {email}\n\nMensaje:\n{mensaje}"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(email_message)
    except Exception as e:
        return jsonify({"error": f"Error al enviar el correo: {str(e)}"}), 500

    return jsonify({"message": "Mensaje enviado correctamente"}), 200

@app.route("/pedidos", methods=["GET"])
def obtener_pedidos():
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pagos ORDER BY id DESC")
        columnas = [col[0] for col in cursor.description]
        pedidos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        cursor.close()
        return jsonify(pedidos)
    except Exception as e:
        print("Error al obtener pedidos:", e)
        return jsonify({"error": "No se pudieron obtener los pedidos"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
