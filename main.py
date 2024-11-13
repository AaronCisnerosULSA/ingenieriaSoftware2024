from flask import Flask, jsonify, request

app = Flask(__name__)

# Endpoint raíz
@app.route("/")
def root():
    return "root"


'''
Crear los endpoints para los siguientes métodos
GET --> Obtener información
POST --> Crear información
PUT --> Actualizar información
DELETE --> Borrar información
'''
# Endpoint para obtener un usuario por ID
@app.route("/users/<user_id>")
def get_user(user_id):
    user = {
        "id": user_id,
        "name": "Aarock",
        "telefono": "57993449"
    }
    query = request.args.get("query")
    if query:
        user["query"] = query
    return jsonify(user), 200

# Endpoint para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    data["status"] = "user created"
    return jsonify(data), 201

# Endpoint para actualizar un usuario
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    updated_user = {
        "id": user_id,
        "name": data.get("name", "Aarock"),  # Valor por defecto si no se envía "name"
        "telefono": data.get("telefono", "57993449"),  # Valor por defecto si no se envía "telefono"
        "status": "user updated"
    }
    return jsonify(updated_user), 200

# Endpoint para borrar un usuario
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    response = {
        "id": user_id,
        "status": "user deleted"
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
