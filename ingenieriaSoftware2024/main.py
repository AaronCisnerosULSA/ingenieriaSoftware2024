from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos
db = SQLAlchemy(app)

# Define el modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

# Crea las tablas en la base de datos (solo la primera vez)
with app.app_context():
    db.create_all()

# Endpoint raíz que ahora usa un template HTML
@app.route("/")
def root():
    return render_template("index.html")

# Endpoint para mostrar todos los usuarios (GET)
@app.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": user.name, "telefono": user.telefono} for user in users]
    return render_template("users.html", users=users_list)

# Endpoint para agregar un nuevo usuario (POST)
@app.route("/users/new", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data = request.form
        new_user = User(name=data['name'], telefono=data['telefono'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('get_users'))
    return render_template("add_user.html")

# Endpoint para editar un usuario existente (PUT)
@app.route("/users/edit/<int:user_id>", methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'POST':
        data = request.form
        user.name = data.get("name", user.name)
        user.telefono = data.get("telefono", user.telefono)
        db.session.commit()
        return redirect(url_for('get_users'))
    return render_template("edit_user.html", user=user)

# Endpoint para eliminar un usuario existente (DELETE)
@app.route("/users/delete/<int:user_id>", methods=['GET'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('get_users'))

if __name__ == '__main__':
    app.run(debug=True)

