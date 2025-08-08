import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, inspect
from alembic import context
from app.infrastructure.database.postgres import Base, engine

# Registro de modelos
from app.domain.models import Product, Supplier, Seller
for model in [Product, Supplier, Seller]:
    model.__table__

    # # verifica si el modelo no se encuentra registrado
    # if not hasattr(model, '__table__'):
    #     model.__table__

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_online():
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
            render_as_batch=True,
            dialect_opts={"paramstyle": "named"},
            transactional_ddl=False
        )
        
        # Verificación de schema antes de migrar
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names(schema='sales_management')
        print(f"Tablas existentes: {existing_tables}")  # Solo para visualización
        
        with context.begin_transaction():
            context.run_migrations()

# 4. Ejecución directa (sin modo offline)
run_migrations_online()