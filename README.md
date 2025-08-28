
# 🚀 API de Insumos con FastAPI y PostgreSQL 

## Descripción

Este proyecto consiste en un CRUD de API´s de testing desarrollada para el proceso de selección de la vacante Python Backend Developer, en la cual se plantea un CRUD para gestionar insumos de alimentos y bebidas para una tienda minorista, almacenándolos en una base de datos **PostgreSQL**.

Como tecnologías de desarrollo se ha utilizado **FastAPI**, **Pydantic** y **Uvicorn**,
para la interacción con la base de datos se plantea el uso de **sqlalchemy** creando migraciones mediante la biblioteca **Alembic**.

A futuro se planea integrar pruebas unitarias en **pytest**, para probar la inserción de datos desde las funciones del controlador con **sqlite3**, inserción y validación de datos con **Pydantic** desde la api con **Uvicorn**.

---
## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener:

✅ **Python 3.11+** instalado.

✅ **Pip y virtualenv** instalados y actualizados.

✅ **Instancia de PostgreSQL** con usuarios con permisos de creación (para PostgreSQL).

Si lo necesitas puedes usar pyenv para manejar diferentes versiones de python

- [Doc](https://github.com/pyenv-win/pyenv-win)
- [Installation](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md)

---
## Environment Variables

Para levantar este proyecto necesitas agregar las siguientes variables a tu **.env** file:

#### Ambientes de desarrollo

`ENVIRONMENT=developmen`

#### PostgreSQL
`POSTGRES_HOST = tu_host`

`POSTGRES_PORT=5432`

`POSTGRES_DB=tu_db`

`POSTGRES_USER=postgres`

`POSTGRES_PASSWORD=tu_password`

`POSTGRES_SCHEMA=tu_schema`

#### Django - Configuración
`DJANGO_SECRET_KEY = tu_django_secret_key`

`ADMIN_PASSWORD=tu_password_admin`

#### Tokens y cifrado

> [!NOTE]
> Nota en los archivos jwt_utils.py y aes_cipher.py cuentas con funciones para generar tu FERNET_KEY y probar las funciones de cifrado

`SECRET_KEY=tu_secret_key`

`FERNET_KEY=tu_fernet_key`

> [!NOTE]
Ingresa el valor que prefieras, si no ingresas este valor por defecto se asigna el valor "/demo/api/v1":

`API_PREFIX = tu_ruta_personalizada` 

## Deployment

**Clonar el repositorio:**

```sh
git clone https://github.com/Santiago-Figu/sales-management.git
cd sales-management
```

**Clonar el repositorio:**

```sh
git clone https://github.com/Santiago-Figu/sales-management.git
cd sales-management
```

## Migraciones


Ejecuta las migraciones actuales:

```sh
  alembic upgrade head
```

> [!NOTE]
> Si quieres crear tus propias Migraciones ejecuta el siguiente comando antes de upgrade head, para crear una nueva migración en la ruta **app\alembic\versions**, pero recuerda que debes apuntar a tuy host local de PostgreSQL, modificando la variable de entorno **POSTGRES_HOST**, cuando ejecutes el contenedor el host debe apuntar al que configuraste para tus contenedores, por defecto docker le asigna el nombre de **postgres**:

```sh
  alembic revision --autogenerate -m "initial migration"
```

## Crear Contenedor Docker

Crear contenedor:
> [!NOTE]
> El nombre del contenedor y la imagen estan configurados en el archivo **docker-compose**:

```sh
    docker-compose build && docker-compose up -d
```

> [!NOTE]
> Si quieres reconstruir el Contenedor, ejecuta:

```sh
  docker-compose down && docker-compose build && docker-compose up -d
```

## Instalación

```sh
cd sales-management
```

**Crear un entorno virtual e instalar dependencias:**

```sh
python -m venv env
```
En Windows run 
```sh
  env\Scripts\activate
```
En Mac run 
```sh
  source env/bin/activate
```
Actualiza tu gestor de paquetes

```sh
  python -m pip install --upgrade pip
```

Instala las dependencias

```sh
  pip install -r requirements.txt
```


---
## API Reference


| Método   | Endpoint                          | Descripción                              |
| -------- | --------------------------------- | ---------------------------------------- |
| `POST`   | `/demo/api/v1/products/`          | Crea un nuevo producto                   |
| `GET`    | `/demo/api/v1/products/`          | Obtiene todos los productos              |
| `GET`    | `/demo/api/v1/products/{product_id}`| Obtiene un productos por id            |
| `PUT`    | `/demo/api/v1/products/{product_id}`| Actualiza un producto existente        |
| `DELETE` | `/demo/api/v1/products/{product_id}`| Elimina un producto  existente         |
| `POST`   | `/demo/api/v1/categories/`          | Crea un nuevo producto                 |
| `GET`    | `/demo/api/v1/categories/`          | Obtiene todos las categoria            |
| `GET`    | `/demo/api/v1/categories/{category_id}`| Obtiene una categoria por id        |
| `PUT`    | `/demo/api/v1/categories/{category_id}`| Actualiza una categoria existente   |
| `DELETE` | `/demo/api/v1/categories/{category_id}`| Elimina una categoria existente     |

---
## Testing

Para correr las pruebas unitarias con **pytest**, ejecuta:

```sh
pytest app/tests/ --verbose
```

Si deseas ver los `print()` en las pruebas, usa:

```sh
pytest -s app/tests/
```

Para ejecutar limpiaando la caché de pytest:

```sh
pytest --cache-clear
```

---
## ToDo

- Agregado de tokens a apis para evitar ejecuciones no autorizadas
- Mejorar modelos de entidades
- Agregar validaciones de datos en apis
- Agregar modelos de Empleados, Proveedores, Roles, Sucursales, Ventas, Detalles Ventas, Facturas
## Authors

- **Autor:** [Santiago Figueroa](https://www.linkedin.com/in/sfigu/)


## Feedback

If you have any feedback, please reach out to us at sfigu@outlook.com

