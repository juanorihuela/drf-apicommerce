# Ecommerce API

API de app Ecommerce generica
+ Productos e inventario
+ Ordenes
+ Detalle de Ordenes

## Estructura del proyecto:
+ Python/Django
+ Rest-Framework
+ PostgreSQL

## Instalación

### entorno y requirements
Activar entorno virtual e instalar requerimientos del sistema dentro de **requirements.txt**
* `python -m venv .venv`
* `pip install -r requirements.txt`

### variables de entorno
Crea el archivo **.env** en la raíz del proyecto con las variables de entorno de settings

Para crear una nueva secret_key usa la función **get_random_secret_key()** en la terminal
* `python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### db
+ Crea la base de datos en tu base local y crea las migraciones del proyecto
    * `python manage.py makemigrations`
    * `python manage.py migrate`

    Si no se generan los modelos de la app puedes generarlos manualmente
    * `python manage.py makemigrations orders`
    * `python manage.py migrate orders`

    **motor postgres: django.db.backends.postgresql_psycopg2**

+ Crea un super usuario y un usuario sin permisos en el panel de admin
    * `python manage.py createsuperuser`

+ Genera un token para el usuario sin permisos en el panel de admin o con el comando drf_create_token
    * `python manage.py drf_create_token tu_username`

## Prueba
Intenta tocar algún endpoint usando GET/POST. Puedes ver los ep y modelos en el directorio de la app 'orders'

### autenticación
Recuerda mandar el token del usuario dentro de los headers de la petición o recibirás un código de error 401
+ `Authorization: Token tu_usertoken`
