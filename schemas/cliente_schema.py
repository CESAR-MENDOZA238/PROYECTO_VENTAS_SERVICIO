import re
from pydantic import BaseModel, field_validator
from typing import Optional

class ClienteCrear(BaseModel):
    nombre:   str
    ruc:      str
    email:    str
    telefono: str

    @field_validator("ruc")
    @classmethod
    def validar_ruc(cls, valor):
        if not re.fullmatch(r"\d{11}", valor):
            raise ValueError("El RUC debe tener exactamente 11 dígitos numéricos")
        return valor
    @field_validator("email")
    def validar_email(cls, valor):
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
            raise ValueError("El email no tiene un formato válido (ej: nombre@dominio.com)")
        return valor
    
class ClienteActualizar(BaseModel):
    nombre:   Optional[str] = None
    email:    Optional[str] = None
    telefono: Optional[str] = None

class ClienteRespuesta(BaseModel):
    id:       int
    nombre:   str
    ruc:      str
    email:    str
    telefono: str