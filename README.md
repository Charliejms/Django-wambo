# How to deploy a Django app with PostgreSQL + Gunicorn + Nginx using pyenv on Ubuntu Server 16.04

 - [Personal gist](https://gist.github.com/Charliejms/87cca982052b5604bdea42d05825fe6e)

## Gist
Instalación Virtual Env

1. Crear el entorno virtual en nombre_usuario/.venv/nombre_proyecto

2. Activar entorno virtual en la raiz:
    ```
    source .venv/nombre_proyecto/bin/activate
    ```
3. Desactivar el entorno virtual:
    ```
    deactivate
    ```
4. Actualizar gestor de paquetes de Django
    ```
    pip install --upgrade pip
    ```
5. **Paso 1** Clonar el repo e instalar los dependencias necesarios:
    ```
    pip install -r requirements.txt
    ```
6. Migrar la base de datos del proyecto
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
7. Crear super usuario
    ```
    python manage.py createsuperuser
    ```
8. **Paso 2** Ejecutar:
    ```
    python manage.py runserver
    ```
