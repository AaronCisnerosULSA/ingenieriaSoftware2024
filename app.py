from flask import Flask, request, redirect, url_for, render_template
from models import db, get_users, get_user, add_user, delete_user, update_user, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')  # Renderizamos el template 'index.html' para el root

@app.route('/users', methods=['GET'])
def users():
    users = get_users()
    return render_template('users.html', users=users)  # Renderizamos la lista de usuarios en 'users.html'

@app.route("/users/new", methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        # Procesar el formulario enviado
        name = request.form.get('name')
        telefono = request.form.get('telefono')

        # Crear un nuevo usuario en la base de datos
        user = add_user(name=name, telefono=telefono)

        # Redirigir a la lista de usuarios después de agregarlo
        return redirect(url_for('users'))

    # Si es una solicitud GET, renderizar el formulario para agregar usuario
    return render_template("add_user.html")

@app.route("/users/edit/<int:user_id>", methods=['GET', 'POST'])
def edit_user_route(user_id):
    # Obtener el usuario por ID
    user = get_user(user_id)
    if not user:
        return {"error": "User not found"}, 404

    if request.method == 'POST':
        # Procesar los datos enviados desde el formulario
        name = request.form.get("name", user.name)
        telefono = request.form.get("telefono", user.telefono)

        # Actualizar los datos del usuario
        user = update_user(user_id=user_id, name=name, telefono=telefono)
        return redirect(url_for('users'))

    # Si es una solicitud GET, renderizar el formulario con los datos del usuario
    return render_template("edit_user.html", user=user)

@app.route("/users/delete/<int:user_id>", methods=['GET'])
def delete_user_route(user_id):
    user = get_user(user_id)
    if not user:
        return {"error": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()

    # Realizar la redirección después de eliminar
    return redirect(url_for('users'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Inicializamos la base de datos
    app.run(debug=True)  # Ejecutamos la app en modo debug
