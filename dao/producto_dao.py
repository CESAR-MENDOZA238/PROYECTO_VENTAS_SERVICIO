import psycopg2
from config.base_datos import obtener_conexion
from config.logger import Logger
from modelos.producto import Producto

class ProductoNoEncontradoError(Exception):
    def __init__(self, prod_id):
        super().__init__(f"Producto ID = {prod_id} no encontrado")
        
class ProductoConVentasError(Exception):
    def __init__(self, producto_id):
        super().__init__(f"Producto ID = {producto_id} no se puede eliminar: tiene ventas asociadas")

class ProductoDAO:
    def __init__(self):
        
        self.__log = Logger()
        
    def buscar(self, prod_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = %s", (prod_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_producto(fila) if fila else None

    def insertar(self, p):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s) RETURNING id",
                       (p.nombre, p.precio,))
        p.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        self.__log.info(f"Producto agregado: {p.nombre} S/.{p.precio:.2f} (ID = {p.id})")
        return p
    
    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY nombre")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_producto(f) for f in filas]
  
    def eliminar(self, prod_id):
        p=self.buscar(prod_id)
        if not p:
            self.__log.error(f"Eliminar fallido: Producto ID = {prod_id} no existe")
            raise ProductoNoEncontradoError(prod_id)

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM productos WHERE id = %s", (prod_id,))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.close()
            self.__log.warning(f"Eliminar fallido: Producto ID = {prod_id} tiene ventas asociadas")
            raise ProductoConVentasError(prod_id)

        self.__log.info(f"Producto eliminado: {p.nombre} (ID = {prod_id})")
        return True
    
    def actualizar(self, prod_id, nombre = None, precio = None):
        p = self.buscar(prod_id)
        if not p:
            self.__log.error(f"Actualizar fallido: Producto ID = {prod_id} no existe")
            raise ProductoNoEncontradoError(prod_id)
        nuevo_nombre = nombre if nombre is not None else p.nombre
        nuevo_precio = precio if precio is not None else p.precio
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE productos SET nombre=%s, precio=%s WHERE id=%s",
            (nuevo_nombre, nuevo_precio, prod_id)
        )
        conn.commit()
        conn.close()
        p.nombre = nuevo_nombre
        p.precio = nuevo_precio
        self.__log.info(f"Producto actualizado: ID = {prod_id}")
        return p
    
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM productos")
        total = cursor.fetchone()["total"]
        conn.close()
        return total
    
    def __fila_a_producto(self, fila):
        p = Producto(fila["nombre"], fila["precio"])
        p.id = fila["id"]
        return p