# Práctica de Flask - Configuración de Base de Datos y Rutas

Este documento detalla la configuración de la base de datos en SQLite, el flujo de retorno de datos a las plantillas HTML, y la creación del entorno virtual para gestionar dependencias del proyecto.

## Índice

1. [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
2. [Rutas y Retorno a Plantillas HTML](#rutas-y-retorno-a-plantillas-html)
3. [Manejo de errores](#manejo-de-errores)
4. [Dificultades](#dificultades)
5. [Anexos](#anexos)

---

### Configuración de la Base de Datos

Usamos SQLite como motor de base de datos para este proyecto. Los pasos incluyen la conexión, configuración de la base de datos, y la creación de una tabla de usuarios con los campos `id`, `name`, `telefono` y `status`.

#### Código para la Configuración

```python
from sqlite3 import connect

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
```

La opción `check_same_thread=False` permite el acceso desde distintos hilos en SQLite.

#### Detalles de la Tabla `users`

- `id`: Clave primaria, autoincrementable.
- `name`: Nombre del usuario, campo de texto obligatorio.
- `telefono`: Teléfono del usuario, campo de texto obligatorio.
- `status`: Estado del usuario (`user created`, `user updated`, o `user deleted`).

---

### Rutas y Retorno a Plantillas HTML

Las rutas principales configuran el flujo entre las operaciones CRUD y las plantillas HTML para el frontend. A continuación se presentan las rutas y su funcionalidad principal.

#### Ruta Principal (`/`)

La ruta raíz (`/`) muestra todos los usuarios cuyo estado no sea `"user deleted"`, usando el template `index.html`.

```python
@app.route("/")
def root():
    cursor.execute("SELECT * FROM users WHERE status != 'user deleted'")
    rows = cursor.fetchall()
    
    column_names = [description[0] for description in cursor.description]
    list_users = [dict(zip(column_names, row)) for row in rows]

    return render_template("index.html", users=list_users)
```

#### Ruta de Detalle de Usuario (`/users/<int:user_id>`)

Muestra los detalles de un usuario específico en `user_detail.html`, o un mensaje de error si el usuario ha sido eliminado.

```python
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
```

#### Otras Rutas para Crear, Editar y Eliminar Usuarios

- **Crear Usuario**: Muestra un formulario en `create_user.html` y agrega el usuario en la base de datos.
- **Actualizar Usuario**: Muestra los detalles en `update_user.html` y permite actualizarlos.
- **Eliminar Usuario**: Cambia el `status` del usuario a `"user deleted"`.

---

### Manejo de errores:

Para manejar los errores de acceso a las rutas, se utilizó la API de [este don](https://github.com/jacebrowning/memegen#special-characters) que permite customizar una imagen de meme para mostrar el codigo de error y un mensaje personalizado, en la parte superior e inferior de la misma.

Se creó esta función en para manejar la correcta construcción del end point:
```python 
helpers.py 

def apology(message, code=400):
    def escape(s):
        """
        Recursos de este man-> https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code
```

La cual recibirá el mensaje y código en main.py.
---

### Dificultades:

1. Lectura de datos desde la db. Tuve que convertir los datos obtenidos de la query del objeto "cursor" con fetchall() y pasarlo a un diccionario obteniendo los nombres de las columnas por aparte con un ciclo y asi sacar las keys.

2. Implementación de la api de la generación de meme para mostrar el codigo de error al usuario. Ya que estaba estructurando mal el end point y la imagen que había escogido en primera instancia no estaba disponible.
---
### Anexos:

Interfaz principal
```markdown
[Descripción de la Imagen](https://github.com/QuesilloLover/ingenieriaSoftware2024/raw/master/static/img/foto1.png)
```
