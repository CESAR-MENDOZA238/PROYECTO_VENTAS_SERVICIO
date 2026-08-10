from datetime import datetime
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.venta import Venta

class VentaNoEncontradaError(Exception):
    def __init__(self, venta_id):
        super().__init__(f"Venta ID={venta_id} no encontrada")

class VentaDAO:
    def __init__(self):
        self.__log = Logger()

    def registrar(self, venta, precio_producto):
        venta.total = round(venta.cantidad * precio_producto, 2)


        venta.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ventas (cliente_id, producto_id, cantidad, fecha, total) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (venta.cliente_id, venta.producto_id, venta.cantidad, venta.fecha, venta.total)
        )
        venta.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Venta registrada: ID={venta.id} Total=S/.{venta.total:.2f}")
        return venta

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        # v.cliente_id y v.producto_id se agregan al SELECT porque
        # VentaRespuesta (schema) los necesita, además de los nombres del JOIN.
        cursor.execute("""
            SELECT v.id, c.nombre AS cliente, p.nombre AS producto,
                   v.cantidad, v.fecha, v.total,
                   v.cliente_id, v.producto_id
            FROM ventas v
            JOIN clientes  c ON v.cliente_id  = c.id
            JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha DESC
        """)
        filas = cursor.fetchall()
        conn.close()
        # dict(f) convierte cada RealDictRow en un dict estándar para que FastAPI lo serialice.
        return [dict(f) for f in filas]

    # NUEVO en semana-14: el router de ventas necesita consultar una venta
    # individual (GET /ventas/{id}), algo que el menú CLI nunca hacía.
    def buscar_por_id(self, venta_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, c.nombre AS cliente, p.nombre AS producto,
                   v.cantidad, v.fecha, v.total,
                   v.cliente_id, v.producto_id
            FROM ventas v
            JOIN clientes  c ON v.cliente_id  = c.id
            JOIN productos p ON v.producto_id = p.id
            WHERE v.id = %s
        """, (venta_id,))
        fila = cursor.fetchone()
        conn.close()
        return dict(fila) if fila else None

    def buscar_por_cliente(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, c.nombre AS cliente, p.nombre AS producto,
                   v.cantidad, v.fecha, v.total,
                   v.cliente_id, v.producto_id
            FROM ventas v
            JOIN clientes  c ON v.cliente_id  = c.id
            JOIN productos p ON v.producto_id = p.id
            WHERE v.cliente_id = %s
            ORDER BY v.fecha DESC
        """, (cliente_id,))
        filas = cursor.fetchall()
        conn.close()
        #convierte JSON a Diccionaro
        return [dict(f) for f in filas]

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM ventas")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def actualizar(self, venta_id, cantidad, precio_producto):
        v = self.buscar_por_id(venta_id)
        if not v:
            self.__log.error(f"Actualizar fallido: Venta ID = {venta_id} no existe")
            raise VentaNoEncontradaError(venta_id)
        nuevo_total = round(cantidad * precio_producto, 2)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE ventas SET cantidad=%s, total=%s WHERE id=%s",
            (cantidad, nuevo_total, venta_id)
        )
        conn.commit()
        conn.close()
        self.__log.info(f"Venta actualizada: ID = {venta_id}")
        return self.buscar_por_id(venta_id)

    def eliminar(self, venta_id):
        v = self.buscar_por_id(venta_id)
        if not v:
            self.__log.error(f"Eliminar fallido: Venta ID = {venta_id} no existe")
            raise VentaNoEncontradaError(venta_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ventas WHERE id = %s", (venta_id,))
        conn.commit()
        conn.close()
        self.__log.info(f"Venta eliminada: ID = {venta_id}")
        return True