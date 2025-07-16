from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    correo = request.form['correo']
    mensaje = request.form['mensaje']

    # Aquí podrías guardar los datos o enviarlos por correo
    print(f"Nombre: {nombre} | Correo: {correo} | Mensaje: {mensaje}")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
