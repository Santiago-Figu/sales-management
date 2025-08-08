
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.core.settings.configdb import settings
from app.core.logger.config import LoggerConfig

# Agregar la ruta del proyecto a sys.path para ejecución local o testing
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# obtener el logger
logger = LoggerConfig(file_name='configPostgreSQL', debug=False).get_logger()


class PostgresqlDataBase():
    dbname = None
    user = None
    password = None
    host = None
    port = None
    schema = None

    def __init__(self):
        self.dbname = settings.POSTGRES_DB
        self.user = settings.POSTGRES_USER
        self.password = settings.POSTGRES_PASSWORD
        self.host = settings.POSTGRES_HOST
        self.port = settings.POSTGRES_PORT
        self.schema = settings.POSTGRES_SCHEMA
    
    @property
    def _dbname(self):
        return self.dbname
    
    @property
    def _host(self):
        return self.host
    
    @property
    def _schema(self):
        return self.schema
    
    def get_url_postgresql(self):
        """Crear la URL de conexión a la base de datos"""
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
    
    def ensure_schema(self, engine):
        """Crea el esquema y otorga permisos"""
        logger.info("Vefificando esquema...")
        try:
            with engine.connect() as conn:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {self._schema}"))
                conn.execute(text(f"GRANT ALL ON SCHEMA {self._schema} TO {self.user}"))
                conn.commit()
        except Exception as e:
            logger.warning("no se aplicarón cambios a la BD...")
            logger.warning(f"Error: {e}")

def get_db():
    """Genera una instancia de sesión para la base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensure_database():
    """Verifica si la base de datos existe y la crea si no existe."""
    from sqlalchemy import inspect

    inspector = inspect(engine)
    if not inspector.get_schema_names():
        Base.metadata.create_all(bind=engine)
        logger.info(f"Base de datos '{PostgresqlDataBase()._dbname}' y tablas creadas exitosamente.")
    else:
         logger.info(f"La base de datos '{PostgresqlDataBase()._dbname}' ya existe.")

def test_connection():
    """Prueba de conexión a la base de datos."""
    status = False
    message = ""
    try:
        # Obtener la conexión desde el engine
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            message= "Conexión a la base de datos exitosa."
            # status = f'{result.fetchone()}'
            status = True
    except SQLAlchemyError as e:
        message = f"Error en la conexión: {e}"
        logger.error(message)
    finally:
        return message, status

engine = create_engine(
    PostgresqlDataBase().get_url_postgresql(),
    connect_args={"options": f"-c search_path={PostgresqlDataBase()._schema}"}
)

message, status = test_connection()
# ensure_database()
logger.info(message)
logger.info(f"Resultado de la consulta: {status}")

# PostgresqlDataBase().ensure_schema(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata  # Exporta también metadata
__all__ = ['Base', 'engine', 'SessionLocal', 'metadata']

logger.info("configuración postgres, terminada")
    
if __name__ == "__main__":
    message, status = test_connection()
    # ensure_database()
    logger.info(message)
    logger.info(f"Resultado de la consulta: {status}")



