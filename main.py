from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.base_datos import inicializar
from routers import clientes, productos, ventas, servicios

app = FastAPI(
    title="Sistema de Gestión POO",
    version="1.0",
    description="API REST para gestión de clientes, productos y ventas",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

inicializar()

app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(ventas.router)
app.include_router(servicios.router)
@app.get("/")
def inicio():
    return {"mensaje": "API TIENDA COMPONENTES ELECTRONICOS POO",
            "version": "1.1",
            "docs": "/docs"
    }