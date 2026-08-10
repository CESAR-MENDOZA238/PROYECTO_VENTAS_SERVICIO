# MODELO - Servicio (soporte técnico)
# Representa una orden de servicio técnico asociada a un cliente.
# Sigue el mismo patrón que Venta: tiene una CLAVE FORÁNEA (cliente_id)
# que hace referencia a la tabla clientes.

class Servicio:
    def __init__(self, cliente_id, equipo_modelo, descripcion_falla,
                 costo_reparacion=0.0, estado="Pendiente",
                 fecha_ingreso=None, fecha_entrega=None):
        self.id = None                          # asignado por PostgreSQL con SERIAL
        self.cliente_id = cliente_id            # FK -> tabla clientes
        self.equipo_modelo = equipo_modelo
        self.descripcion_falla = descripcion_falla
        self.costo_reparacion = costo_reparacion
        self.estado = estado                    # Pendiente / En proceso / Entregado
        self.fecha_ingreso = fecha_ingreso
        self.fecha_entrega = fecha_entrega

    def __str__(self):
        return (f"[{self.id}] Cliente ID = {self.cliente_id} | "
                f"{self.equipo_modelo} | Estado: {self.estado}")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "equipoModelo": self.equipo_modelo,
            "descripcionFalla": self.descripcion_falla,
            "costoReparacion": self.costo_reparacion,
            "estado": self.estado,
            "fechaIngreso": self.fecha_ingreso,
            "fechaEntrega": self.fecha_entrega,
        }
