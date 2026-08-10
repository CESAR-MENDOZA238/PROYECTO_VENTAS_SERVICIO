from datetime import datetime
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.servicio import Servicio


class ServicioNoEncontradoError(Exception):
    def __init__(self, servicio_id):
        super().__init__(f"Servicio ID={servicio_id} no encontrado")


class ServicioDAO:
    def __init__(self):
        self.__log = Logger()

    def registrar(self, servicio):
        servicio.fecha_ingreso = servicio.fecha_ingreso or datetime.now().strftime("%Y-%m-%d")
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO servicios
               (cliente_id, equipo_modelo, descripcion_falla, costo_reparacion,
                estado, fecha_ingreso, fecha_entrega)
               VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            (servicio.cliente_id, servicio.equipo_modelo, servicio.descripcion_falla,
             servicio.costo_reparacion, servicio.estado, servicio.fecha_ingreso,
             servicio.fecha_entrega)
        )
        servicio.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Servicio registrado: ID={servicio.id} Cliente={servicio.cliente_id}")
        return servicio

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.cliente_id, c.nombre AS cliente, s.equipo_modelo,
                   s.descripcion_falla, s.costo_reparacion, s.estado,
                   s.fecha_ingreso, s.fecha_entrega
            FROM servicios s
            JOIN clientes c ON s.cliente_id = c.id
            ORDER BY s.fecha_ingreso DESC
        """)
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_dict(f) for f in filas]

    def buscar_por_id(self, servicio_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.cliente_id, c.nombre AS cliente, s.equipo_modelo,
                   s.descripcion_falla, s.costo_reparacion, s.estado,
                   s.fecha_ingreso, s.fecha_entrega
            FROM servicios s
            JOIN clientes c ON s.cliente_id = c.id
            WHERE s.id = %s
        """, (servicio_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_dict(fila) if fila else None

    def actualizar(self, servicio_id, equipo_modelo=None, descripcion_falla=None,
                    costo_reparacion=None, estado=None, fecha_entrega=None):
        actual = self.buscar_por_id(servicio_id)
        if not actual:
            self.__log.error(f"Actualizar fallido: Servicio ID = {servicio_id} no existe")
            raise ServicioNoEncontradoError(servicio_id)

        nuevo_equipo = equipo_modelo if equipo_modelo is not None else actual["equipoModelo"]
        nueva_falla = descripcion_falla if descripcion_falla is not None else actual["descripcionFalla"]
        nuevo_costo = costo_reparacion if costo_reparacion is not None else actual["costoReparacion"]
        nuevo_estado = estado if estado is not None else actual["estado"]
        nueva_entrega = fecha_entrega if fecha_entrega is not None else actual["fechaEntrega"]

        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE servicios
               SET equipo_modelo=%s, descripcion_falla=%s, costo_reparacion=%s,
                   estado=%s, fecha_entrega=%s
               WHERE id=%s""",
            (nuevo_equipo, nueva_falla, nuevo_costo, nuevo_estado, nueva_entrega, servicio_id)
        )
        conn.commit()
        conn.close()
        self.__log.info(f"Servicio actualizado: ID = {servicio_id}")
        return self.buscar_por_id(servicio_id)

    def eliminar(self, servicio_id):
        s = self.buscar_por_id(servicio_id)
        if not s:
            self.__log.error(f"Eliminar fallido: Servicio ID = {servicio_id} no existe")
            raise ServicioNoEncontradoError(servicio_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM servicios WHERE id = %s", (servicio_id,))
        conn.commit()
        conn.close()
        self.__log.info(f"Servicio eliminado: ID = {servicio_id}")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM servicios")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def __fila_a_dict(self, fila):
        return {
            "id": fila["id"],
            "cliente_id": fila["cliente_id"],
            "cliente": fila["cliente"],
            "equipoModelo": fila["equipo_modelo"],
            "descripcionFalla": fila["descripcion_falla"],
            "costoReparacion": float(fila["costo_reparacion"]),
            "estado": fila["estado"],
            "fechaIngreso": fila["fecha_ingreso"],
            "fechaEntrega": fila["fecha_entrega"],
        }
