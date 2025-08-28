from fastapi import FastAPI
from app.core.settings.configdb import settings
from app.infrastructure.api.v1.routers.products import router as products_router
from app.infrastructure.api.v1.routers.categories import router as categories_router
from app.infrastructure.api.v1.routers.barcode import router as barcode_router
from app.infrastructure.database.postgres import Base, engine
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sales Management System",
    description= "API for managing sales, products, sellers an suppliers",
    version="1.0.0"
)

app.include_router(products_router,prefix=settings.API_PREFIX)
app.include_router(categories_router,prefix=settings.API_PREFIX)
app.include_router(barcode_router,prefix=settings.API_PREFIX)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
