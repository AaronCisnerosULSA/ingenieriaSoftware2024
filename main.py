from flask import Flask, render_template, request, redirect, url_for
from sqlite3 import connect
from helpers import apology

app = Flask(__name__)

# Configuración de la base de datos
con = connect("database.db", check_same_thread=False)
cursor = con.cursor()

# Creación de la tabla users
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        telefono TEXT NOT NULL,
        status VARCHAR(20) NOT NULL
    )
""")
con.commit()

# Página principal que lista todos los usuarios 
@app.route("/")
def root():
    cursor.execute("SELECT * FROM users WHERE status != 'user deleted'")
    rows = cursor.fetchall()
    
    column_names = [description[0] for description in cursor.description]
    list_users = [dict(zip(column_names, row)) for row in rows]

    return render_template("index.html", users=list_users)

# Página de detalle de un usuario 
@app.route("/users/<int:user_id>")
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ? AND status != 'user deleted'", (user_id,))
    row = cursor.fetchone()
    if row:
        column_names = [description[0] for description in cursor.description]
        user = dict(zip(column_names, row))
        return render_template("user_detail.html", user=user)
    else:
        return apology("Sos necio vos", 404)

# Página para crear un nuevo usuario
@app.route('/users', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        data = request.form
        cursor.execute("INSERT INTO users (name, telefono, status) VALUES (?, ?, ?)",
                       (data["name"], data["telefono"], "user created"))
        con.commit()
        return redirect(url_for("root"))
    return render_template("create_user.html")

# Página para actualizar un usuario
@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'POST':
        data = request.form
        cursor.execute("UPDATE users SET name = ?, telefono = ?, status = ? WHERE id = ?",
                       (data["name"], data["telefono"], "user updated", user_id))
        con.commit()
        
        return redirect(url_for("root"))

    cursor.execute("SELECT * FROM users WHERE id = ? AND status != 'user deleted'", (user_id,))
    row = cursor.fetchone()
    if row:
        column_names = [description[0] for description in cursor.description]
        user = dict(zip(column_names, row))
        return render_template("update_user.html", user=user)
    else:
        return apology("Nada tenes que ver aca", 404)

# Página para eliminar un usuario 
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    cursor.execute("UPDATE users SET status = 'user deleted' WHERE id = ?", (user_id,))
    con.commit()
    return redirect(url_for("root"))


if __name__ == '__main__':
    app.run(debug=True)
