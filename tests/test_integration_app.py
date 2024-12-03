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

def test_add_user_render_template(client):
    """Prueba que la solicitud GET renderice el template 'add_user.html'."""
    response = client.get('/users/new')

    # Verificar que la respuesta es exitosa
    assert response.status_code == 200

    # Verificar que el template correcto se está renderizando
    assert b"<form" in response.data  # Verifica que hay un formulario en el HTML
    assert b"Agregar Usuario" in response.data  # Cambia según el texto presente en tu template


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

def test_edit_user_route_user_exists(client):
    """Prueba que se pueda editar un usuario existente."""
    # Crear un usuario para editar
    with app.app_context():
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
    with app.app_context():
        updated_user = User.query.get(user_id)
        assert updated_user.name == "Jane Doe"
        assert updated_user.telefono == "987654321"


def test_edit_user_route_user_not_found(client):
    """Prueba que devuelve un error 404 si el usuario no existe."""
    # Intentar editar un usuario con un ID inexistente
    non_existent_user_id = 9999
    response = client.post(f'/users/edit/{non_existent_user_id}', data={
        'name': 'Jane Doe',
        'telefono': '987654321'
    })

    # Verificar que devuelve un error 404
    assert response.status_code == 404
    assert b"User not found" in response.data


def test_edit_user_render_template(client):
    """Prueba que la solicitud GET renderice el template 'edit_user.html' con los datos del usuario."""
    with app.app_context():
        # Crear un usuario para la prueba
        new_user = User(name="John Doe", telefono="123456789")
        db.session.add(new_user)
        db.session.commit()

        # Obtener el ID del usuario creado
        user_id = new_user.id

    # Hacer una solicitud GET a la ruta de edición
    response = client.get(f'/users/edit/{user_id}')

    # Verificar que la respuesta es exitosa
    assert response.status_code == 200

    # Verificar que el template correcto se está renderizando
    assert b"<form" in response.data  # Verifica que hay un formulario en el HTML
    assert b"John Doe" in response.data  # Verifica que el nombre está presente
    assert b"123456789" in response.data  # Verifica que el teléfono está presente


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

def test_delete_user_not_found(client):
    """Prueba que devuelve un error 404 si el usuario a eliminar no existe."""
    non_existent_user_id = 9999  # ID de usuario que no existe en la base de datos
    response = client.get(f'/users/delete/{non_existent_user_id}')

    # Verificar que devuelve un error 404
    assert response.status_code == 404
    assert b"User not found" in response.data

def test_app_initialization():
    """Prueba que la base de datos se inicializa correctamente cuando se ejecuta el bloque principal."""
    # Configura la aplicación en modo de prueba
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        # Llama a la inicialización manual de la base de datos
        db.create_all()

        # Verifica que la base de datos se ha creado correctamente
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        assert 'user' in tables  # Cambia 'user' al nombre correcto de tu tabla

        # Limpia la base de datos después de la prueba
        db.drop_all()

