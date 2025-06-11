from flask import Flask, jsonify, redirect, render_template, request, url_for
import os
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta, timezone
import secrets

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  

# Configuración MySQL para Aiven
app.config["MYSQL_USER"] = os.getenv("AVN_USER", "avnadmin")
app.config["MYSQL_PASSWORD"] = os.getenv("AVN_PASSWORD")
app.config["MYSQL_HOST"] = os.getenv("AVN_HOST")
app.config["MYSQL_PORT"] = int(os.getenv("AVN_PORT", "12345"))
app.config["MYSQL_DB"] = os.getenv("AVN_DB", "defaultdb")
app.config["MYSQL_SSL_CA"] = os.getenv("AVN_SSL_CA", "tfg/backend/ca.pem")
app.config["MYSQL_SSL_VERIFY_CERT"] = True 

mysql = MySQL(app)

CORS(app, resources={r"/*": {"origins": "https://detallspatch.onrender.com/"}}, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

class User(UserMixin):
    def __init__(self, id_, email):
        self.id = id_
        self.email = email
    
    def is_admin(self):
        if not self.is_authenticated:
            return False
        return self.email == "pedritoue2@gmail.com"
    
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
@login_required
def add_product():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    if not current_user.is_admin():
        return jsonify({'error': 'No autorizado'}), 403

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos JSON no proporcionados'}), 400

        required_fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Faltan campos obligatorios'}), 400

        try:
            precio = float(data['precio'])
            stock = int(data['stock'])
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Datos numéricos inválidos: {str(e)}'}), 400

        cursor = mysql.connection.cursor()
        
        print("Valores a insertar:", {
            'nombre': data['nombre'],
            'descripcion': data['descripcion'],
            'precio': precio,
            'stock': stock,
            'imagen': data['imagen']
        })

        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio, stock, imagen) VALUES (%s, %s, %s, %s, %s)",
            (data['nombre'], data['descripcion'], precio, stock, data['imagen'])
        )
        
        mysql.connection.commit()
        product_id = cursor.lastrowid
        cursor.close()

        return jsonify({
            'message': 'Producto añadido correctamente',
            'product_id': product_id
        }), 201

    except Exception as e:
        if 'mysql.connection' in locals():
            mysql.connection.rollback()
        if 'cursor' in locals():
            cursor.close()
        
        print("Error completo:", str(e))
        
        return jsonify({
            'error': 'Error al añadir producto',
            'details': str(e)
        }), 500

@app.route('/admin/<int:producto_id>', methods=['DELETE'])
@login_required
def delete_product(producto_id):
    if not current_user.is_admin():
        return jsonify({'error': 'No autorizado'}), 403

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

@app.route("/recuperar", methods=["POST"])
def recuperar_contraseña():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email requerido"}), 400

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Correo no registrado"}), 404

    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)

    cursor.execute("INSERT INTO reset_tokens (email, token, expires_at) VALUES (%s, %s, %s)",
                   (email, token, expires_at))
    conn.commit()
    cursor.close()

    reset_link = f"https://detallspatch.onrender.com/resetear/{token}"

    email_message = EmailMessage()
    email_message["Subject"] = "Recuperación de contraseña"
    email_message["From"] = os.getenv("EMAIL_SENDER")
    email_message["To"] = email
    email_message.set_content(
        f"Haz clic en este enlace para restablecer tu contraseña:\n\n{reset_link}\n\nEste enlace expirará en 1 hora."
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(email_message)
    except Exception as e:
        return jsonify({"error": f"Error al enviar el correo: {str(e)}"}), 500

    return jsonify({"message": "Correo de recuperación enviado"}), 200


@app.route("/resetear/<token>", methods=["GET", "POST"])
def resetear_contraseña(token):
    conn = mysql.connection
    cursor = conn.cursor()

    cursor.execute("SELECT email, expires_at FROM reset_tokens WHERE token = %s", (token,))
    result = cursor.fetchone()

    if not result:
        cursor.close()
        return jsonify({"error": "Token inválido"}), 400

    email, expires_at = result

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) > expires_at:
        cursor.close()
        return jsonify({"error": "Token expirado"}), 400

    if request.method == "GET":
        cursor.close()
        return jsonify({"message": "Token válido", "email": email}), 200

    if request.method == "POST":
        data = request.get_json()
        nueva_clave = data.get("password")

        if not nueva_clave:
            cursor.close()
            return jsonify({"error": "Contraseña requerida"}), 400

        try:
            hashed_password = generate_password_hash(nueva_clave)

            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
            cursor.execute("DELETE FROM reset_tokens WHERE token = %s", (token,))
            conn.commit()
            cursor.close()
            return jsonify({"message": "Contraseña actualizada correctamente"}), 200
        except Exception as e:
            cursor.close()
            print("Error actualizando contraseña:", e)
            return jsonify({"error": "Error al actualizar la contraseña"}), 500
        
@login_manager.unauthorized_handler
def unauthorized():
    if request.accept_mimetypes.accept_json or request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"error": "No autorizado"}), 401
    return redirect(url_for('login'))   

@app.errorhandler(404)
def not_found(error):
    if request.accept_mimetypes.accept_html:
        return render_template("404.html"), 404
    return jsonify({"error": "La ruta solicitada no existe"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True,port="1000")
