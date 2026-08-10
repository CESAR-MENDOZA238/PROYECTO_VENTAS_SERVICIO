import psycopg2
from config.logger import Logger
from config.base_datos import obtener_conexion
from modelos.cliente import Cliente

class ClienteNoEncontradoError(Exception):
    def __init__(self, id):
        super().__init__(f"Cliente ID = {id} no encontrado")
        # super().__init__() llama al constructor de Exception
        # con nuestro mensaje personalizado

class RUCDuplicadoError(Exception):
    def __init__(self, ruc):
        super().__init__(f"RUC '{ruc}' ya registrado")

class ClienteConVentasError(Exception):
    def __init__(self, cliente_id):
        super().__init__(f"Cliente ID = {cliente_id} no se puede eliminar: tiene ventas asociadas")

class ClienteDAO:
    def __init__(self):
        self.__log = Logger()
        
    def buscar_por_ruc(self, ruc):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE ruc = %s", (ruc,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_cliente(fila) if fila else None

    def buscar_por_id(self, cliente_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_cliente(fila) if fila else None

    def insertar(self, cliente):
# Paso 1: Verificar que el RUC no esté duplicado
        if self.buscar_por_ruc(cliente.ruc):
            self.__log.warning(f"RUC duplicado: {cliente.ruc}")
            raise RUCDuplicadoError(cliente.ruc)   # Lanza excepción si ya existe

# Paso 2: Guardar en la base de datos SQL
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO clientes (nombre, ruc, email, telefono) VALUES (%s, %s, %s, %s) RETURNING id",
            (cliente.nombre, cliente.ruc, cliente.email, cliente.telefono)
        )
        cliente.id = cursor.fetchone()["id"]
        conn.commit()
        conn.close()
        # Paso 4: Devolver el cliente ya con ID
        self.__log.info(f"Cliente agregado: {cliente.nombre} (ID = {cliente.id})")
        return cliente

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes ORDER BY nombre")
        fila = cursor.fetchall()
        conn.close()
        return [self.__fila_a_cliente(f) for f in fila]
    
    def eliminar(self, cliente_id):
        c=self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Eliminar fallido: Cliente ID = {cliente_id} no existe")
            raise ClienteNoEncontradoError(cliente_id)
        
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.close()
            self.__log.warning(f"Eliminar fallido: Cliente ID = {cliente_id} tiene ventas asociadas")
            raise ClienteConVentasError(cliente_id)
        self.__log.info(f"Cliente eliminado: {c.nombre} (ID = {cliente_id})")
        return True
    
    def actualizar(self, cliente_id, nombre = None, email = None, telefono = None):
        c = self.buscar_por_id(cliente_id)
        if not c:
            self.__log.error(f"Actualizar fallido: Cliente ID = {cliente_id} no existe")
            raise ClienteNoEncontradoError(cliente_id)
        nuevo_nombre = nombre if nombre is not None else c.nombre
        nuevo_email = email if email is not None else c.email
        nuevo_telefono = telefono if telefono is not None else c.telefono
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE clientes SET nombre=%s, email=%s, telefono=%s WHERE id=%s",
            (nuevo_nombre, nuevo_email, nuevo_telefono, cliente_id)
        )
        conn.commit()
        conn.close()
        c.nombre = nuevo_nombre
        c.email = nuevo_email
        c.telefono = nuevo_telefono

        self.__log.info(f"Cliente actualizado: ID = {cliente_id}")
        return c
    
    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM clientes")
        total = cursor.fetchone()["total"]
        conn.close()
        return total
    
    def __fila_a_cliente(self, fila):
        c = Cliente(fila["nombre"], fila["ruc"], fila["email"], fila["telefono"])
        c.id = fila["id"]
        return c