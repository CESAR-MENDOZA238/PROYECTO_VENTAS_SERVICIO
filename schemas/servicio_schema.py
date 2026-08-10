from pydantic import BaseModel, field_validator
from typing import Optional


class ServicioCrear(BaseModel):
    cliente_id: int
    equipoModelo: str
    descripcionFalla: str
    costoReparacion: float = 0.0
    estado: str = "Pendiente"
    fechaEntrega: Optional[str] = None

    @field_validator("costoReparacion")
    @classmethod
    def validar_costo(cls, valor):
        if valor < 0:
            raise ValueError("El costo de reparación no puede ser negativo")
        return valor


class ServicioActualizar(BaseModel):
    equipoModelo: Optional[str] = None
    descripcionFalla: Optional[str] = None
    costoReparacion: Optional[float] = None
    estado: Optional[str] = None
    fechaEntrega: Optional[str] = None


class ServicioRespuesta(BaseModel):
    id: int
    cliente_id: int
    cliente: str
    equipoModelo: str
    descripcionFalla: str
    costoReparacion: float
    estado: str
    fechaIngreso: str
    fechaEntrega: Optional[str] = None
