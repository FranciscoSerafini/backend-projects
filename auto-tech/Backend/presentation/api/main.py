from fastapi import FastAPI
from presentation.api.endpoints.cliente_endpoints import router as cliente_router

app = FastAPI()

# Registrar los routers
app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)