import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
from logging.config import fileConfig

from sqlalchemy import inspect
from alembic import context
from app.infrastructure.database.postgres import Base, engine
from app.core.settings.configdb import settings

# Importación de modelos se supone que alembic lo detecta automaticamente para crear la migración
# En mi caso no lo hacía haci que use la funcion 
from app.domain.models.category import Category
from app.domain.models.product import Product
from app.domain.models.user import User


def create_models():
    """Función que fuerza el registro de todos los modelos solo en casos desesperados"""
    for model in [Category, Product, User]:
        if not hasattr(model, '__table__'):
            raise RuntimeError(f"Modelo {model.__name__} no está correctamente definido")
        # Fuerza la creación/registro de la tabla
        model.__table__.create(bind=engine, checkfirst=False)
        print(f"Modelo {model.__name__} registrado - Tabla: {model.__tablename__}")


def registered_models():
    """Función que fuerza el registro de modelos en metadata sin crear las tablas"""
    # creación de los objetos Table
    for table in [Product, Category, User]:
        Base.metadata._add_table(table.__tablename__, table.__table__.schema, table.__table__)
    
    print("\nTablas registradas en metadata:")
    for table in Base.metadata.sorted_tables:
        print(f"- {table.schema}.{table.name} (columns: {table.columns.keys()})")



# Configura el esquema
Base.metadata.schema = settings.POSTGRES_SCHEMA

registered_models()

# Configuración de Alembic
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online():
    with engine.begin() as connection:
        # DEBUG: Verifica tablas en la base de datos
        inspector = inspect(connection)
        print(f"\nTablas existentes en BD ({settings.POSTGRES_SCHEMA}):")
        for table in inspector.get_table_names(schema=settings.POSTGRES_SCHEMA):
            print(f"- {table}")

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
            render_as_batch=True,
            dialect_opts={"paramstyle": "named"},
            transactional_ddl=False,
            transaction_per_migration=True
        )

         # Debug adicional
        print("\nEjecutando migraciones...")
        with context.begin_transaction():
            context.run_migrations()
        
        # Verificación post-migración
        print("\nTablas después de migración:")
        for table in inspector.get_table_names(schema=settings.POSTGRES_SCHEMA):
            print(f"- {table}")

run_migrations_online()