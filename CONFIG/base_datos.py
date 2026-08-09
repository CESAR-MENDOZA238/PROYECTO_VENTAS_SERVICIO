import sqlite3


ARCHIVO_BD = "sistema.db"
def obtener_conexion():
# sqlite3.connect() abre (o crea si no existe) el archivo de base de datos.

    conn = sqlite3.connect(ARCHIVO_BD)

    conn.row_factory = sqlite3.Row
    return conn

def inicializar():

    conn = obtener_conexion()
    cursor = conn.cursor()

    # Tabla de clientes: ruc tiene restricción UNIQUE para evitar duplicados a nivel de BD.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        ruc TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        telefono TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
        )
    """)
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            total REAL NOT NULL,
            fecha DATE NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES cliente(id),
            FOREIGN KEY (producto_id) REFERENCES producto(id)
        )
    """)
    
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicio_tecnico(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Servicio_ID INTEGER PRIMARY KEY,
            Cliente_ID INTEGER NOT NULL,
            EquipoModelo TEXT NOT NULL,
            DescripcionFalla TEXT NOT NULL,
            CostoReparacion REAL NOT NULL,
            Estado TEXT NOT NULL,
            FechaIngreso DATE NOT NULL,
            FechaEntrega DATE NOT NULL,

            FOREIGN KEY (Cliente_ID) REFERENCES cliente(Cliente_ID)
        )
    """)
    
    # conn.commit() confirma todos los cambios (equivale a "guardar" en la BD).
    # Sin commit(), los cambios se pierden al cerrar la conexión.

        

    conn.commit()
    conn.close()