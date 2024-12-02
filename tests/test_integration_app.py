import pytest
from app import app, db, User

@pytest.fixture
def client():
    # Configura el entorno de pruebas
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Crea el contexto de la aplicación y la base de datos
    with app.app_context():
        db.create_all()  # Crea tablas en la base de datos en memoria
        with app.test_client() as client:
            yield client

def test_root(client):
    """Prueba que el endpoint raíz devuelve el template correcto."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Bienvenido" in response.data  # Cambia según el texto en tu index.html

def test_add_user(client):
    """Prueba agregar un usuario."""
    response = client.post("/users/new", data={"name": "Juan", "telefono": "123456789"})
    assert response.status_code == 302  # Redirección tras agregar
    # Verifica que el usuario se haya agregado en la base de datos
    with app.app_context():
        user = User.query.filter_by(name="Juan").first()
        assert user is not None
        assert user.telefono == "123456789"

def test_get_users(client):
    """Prueba obtener la lista de usuarios."""
    # Agrega un usuario de ejemplo
    with app.app_context():
        db.session.add(User(name="Ana", telefono="987654321"))
        db.session.commit()
    response = client.get("/users")
    assert response.status_code == 200
    assert b"Ana" in response.data  # Cambia según el template de users.html

def test_edit_user(client):
    # Crear un usuario para editar
    new_user = User(name="John Doe", telefono="123456789")
    db.session.add(new_user)
    db.session.commit()

    # Obtener el ID del nuevo usuario
    user_id = new_user.id

    # Realizar la edición
    response = client.post(f'/users/edit/{user_id}', data={
        'name': 'Jane Doe',
        'telefono': '987654321'
    })

    # Verificar que la redirección fue exitosa
    assert response.status_code == 302  # Código de redirección

    # Verificar que los datos fueron actualizados
    updated_user = User.query.get(user_id)
    assert updated_user.name == "Jane Doe"
    assert updated_user.telefono == "987654321"

def test_delete_user(client):
    # Crear un usuario para eliminar
    new_user = User(name="John Doe", telefono="123456789")
    db.session.add(new_user)
    db.session.commit()

    # Obtener el ID del nuevo usuario
    user_id = new_user.id

    # Realizar la eliminación
    response = client.get(f'/users/delete/{user_id}')  # Usamos GET porque en la app el DELETE se simula con un GET

    # Verificar que la redirección fue exitosa
    assert response.status_code == 302  # Código de redirección

    # Verificar que el usuario fue eliminado de la base de datos
    deleted_user = User.query.get(user_id)
    assert deleted_user is None  # El usuario ya no debe existir
