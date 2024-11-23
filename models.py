from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

# Lógica de base de datos movida a funciones
def get_users():
    return User.query.all()

def get_user(user_id):
    return User.query.get(user_id)

def add_user(name, telefono):
    new_user = User(name=name, telefono=telefono)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return user
    return None

def update_user(user_id, name, telefono):
    user = User.query.get(user_id)
    if user:
        user.name = name
        user.telefono = telefono
        db.session.commit()
        return user
    return None
