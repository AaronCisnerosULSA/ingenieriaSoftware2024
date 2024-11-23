from flask import Flask, request, redirect, url_for
from models import db, get_users, get_user, add_user, delete_user, update_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/users', methods=['GET'])
def users():
    users = get_users()
    return {"users": [{"id": u.id, "name": u.name, "telefono": u.telefono} for u in users]}

@app.route('/users/new', methods=['POST'])
def add_user_route():
    name = request.form['name']
    telefono = request.form['telefono']
    user = add_user(name, telefono)
    return redirect(url_for('users'))

@app.route('/users/edit/<int:user_id>', methods=['POST'])
def edit_user_route(user_id):
    name = request.form['name']
    telefono = request.form['telefono']
    user = update_user(user_id, name, telefono)
    if user:
        return redirect(url_for('users'))
    return {"error": "User not found"}, 404

@app.route('/users/delete/<int:user_id>', methods=['GET'])
def delete_user_route(user_id):
    user = delete_user(user_id)
    if user:
        return redirect(url_for('users'))
    return {"error": "User not found"}, 404
