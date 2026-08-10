from pydantic import BaseModel, field_validator
from typing import Optional

class ProductoCrear(BaseModel):
    nombre: str
    precio: float
    
    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor):
        if valor <=0:
            raise ValueError("El precio debe ser mayor que cero")
        return valor

class ProductoActualizar(BaseModel):
    nombre: Optional[str]   = None
    precio: Optional[float] = None

class ProductoRespuesta(BaseModel):
    id:     int
    nombre: str
    precio: float