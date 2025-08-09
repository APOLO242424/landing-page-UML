import platform
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# --- CONFIGURACIÓN DESDE VARIABLES DE ENTORNO ---

# Carga la SECRET_KEY desde el entorno.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_APP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = ('D&S Personalizaciones', os.environ.get('MAIL_USERNAME'))

# Inicializa la extensión Mail
mail = Mail(app)


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/productos/<categoria>')
def galeria_productos(categoria):
    """Muestra una galería de productos para una categoría específica."""
    imagenes_path = os.path.join(app.static_folder, 'imagenes', categoria)

    try:
        # Lista solo los archivos que son imágenes
        imagenes = [f for f in os.listdir(imagenes_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    except FileNotFoundError:
        # Si la carpeta de la categoría no existe, muestra un error 404
        return "Categoría no encontrada", 404

    return render_template('productos.html', categoria=categoria.capitalize(), imagenes=imagenes)


@app.route('/enviar', methods=['POST'])
def enviar():
    """Envía un correo electrónico desde el formulario de contacto."""
    nombre = request.form['nombre']
    correo_origen = request.form['correo']
    mensaje = request.form['mensaje']
    destinatario = app.config['MAIL_USERNAME']

    try:
        msg = Message(
            subject=f"Nuevo mensaje de contacto de: {nombre}",
            recipients=[destinatario],
            body=f"De: {nombre} <{correo_origen}>\n\n{mensaje}"
        )
        mail.send(msg)
        flash('¡Mensaje enviado correctamente! Gracias por contactarnos.', 'success')
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        flash('Hubo un error al enviar el mensaje. Por favor, inténtalo de nuevo.', 'error')

    return redirect(url_for('index') + '#contacto')


if __name__ == "__main__":  
     # Check the System Type before to decide to bind
     # If the system is a Linux machine -:) 
     if platform.system() == "Linux":
        app.run(host='0.0.0.0',port=5000, debug=True)
     # If the system is a windows /!\ Change  /!\ the   /!\ Port
     elif platform.system() == "Windows":
        app.run(host='0.0.0.0',port=50000, debug=True)