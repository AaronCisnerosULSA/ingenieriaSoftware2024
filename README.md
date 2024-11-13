<<<<<<< HEAD
# ingenieriaSoftware2024
Repositorio para la asignatura de Ingeniería de Software IIIC2024 ULSA
=======
# Proyecto Tienda Online

Este proyecto es una API de ejemplo desarrollada en Flask para demostrar cómo pasar de un diseño básico a una implementación interactiva con endpoints REST. 
Más adelante, se añade soporte para bases de datos y se documenta cada fase del proceso.

## Estructura del Proyecto

- **main.py**: Archivo principal que contiene el código de la API.
- **venv**: Entorno virtual que contiene las dependencias del proyecto.

## Requisitos

- **Python 3.8+**
- **Flask** (instalado en el entorno virtual)
- **Git** para el control de versiones.

## Instrucciones de Instalación

1. Clona el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd tiendaOnline

2. Activa el entorno virtual (asegúrate de tener Python 3.8 o superior):

  En Windows:
  venv\Scripts\activate

  En MacOS/Linux:
  source venv/bin/activate
  
3. Instala las dependencias:
  pip install -r requirements.txt

4. Ejecuta la aplicación
La aplicación debería estar corriendo en http://127.0.0.1:5000

Guía de Endpoints
Endpoints Básicos (Rama main)
  GET /users/<user_id>: Devuelve información del usuario.
  Parámetro user_id: ID del usuario que se busca.
  
  POST /users: Crea un nuevo usuario.
  Cuerpo de la solicitud (JSON): Información del usuario.
  Endpoints con Base de Datos (Rama bbdd-version) 
  
Endpoints con Base de Datos (Rama bbdd-version)
(Para esta versión, asegúrate de cambiar a la rama bbdd-version e instalar las dependencias necesarias para el uso de SQLAlchemy).

Notas por Etapas
Etapa 1: Implementación de endpoints básicos sin bases de datos (en la rama main).
Etapa 2: Añadir soporte para bases de datos con SQLAlchemy (en la rama bbdd-version).

Recursos de Aprendizaje
  Flask Documentation
  Git Guide
  SQLAlchemy Documentation
>>>>>>> c025feea3137cf164f29f9397696841bf67be502
