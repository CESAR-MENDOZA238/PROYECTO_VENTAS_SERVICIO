from pydantic import BaseModel, field_validator

class VentaCrear(BaseModel):
    cliente_id:  int
    producto_id: int
    cantidad:    int

    @field_validator("cantidad")
    @classmethod
    def validar_cantidad(cls, valor):
        if valor <=0:
            raise ValueError("La cantidad debe ser mayor que cero")
        return valor

class VentaActualizar(BaseModel):
    cantidad: int

    @field_validator("cantidad")
    @classmethod
    def validar_cantidad(cls, valor):
        if valor <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        return valor


class VentaRespuesta(BaseModel):
    id:          int
    cliente_id:  int
    producto_id: int
    cliente:     str
    producto:    str
    cantidad:    int
    fecha:       str
    total:       float