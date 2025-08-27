# sales-management
Proyecto de CRUD para gestionar ventas de productos, almacenándo los datos en PostgreSQL y MongoDB

#
docker-compose down && docker-compose build && docker-compose up -d

# Generar migations
alembic revision --autogenerate -m "Adding Datetime attributes"

# Aplicar migrations
alembic upgrade head