import sqlite3
ARCHIVO_BD = "sistema.db"
def obtener_conexion():

    conn = sqlite3.connect(ARCHIVO_BD)

    conn.row_factory = sqlite3.Row
    return conn

def inicializar():

    conn = obtener_conexion()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
        Cliente_ID TEXT PRIMARY KEY,
        Nombre TEXT NOT NULL,
        Telefono TEXT UNIQUE NOT NULL,
        Email TEXT NOT NULL
         )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
        Producto_ID TEXT PRIMARY KEY,
        NombreProducto TEXT NOT NULL,
        Descripcion TEXT NOT NULL,
        Precio REAL NOT NULL,
        Stock INTEGER NOT NULL
        )
    """)
    
        
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venta (
            Venta_ID TEXT PRIMARY KEY,
            Cliente_ID TEXT NOT NULL,
            Producto_ID TEXT NOT NULL,
            Cantidad INTEGER NOT NULL,
            TotalVenta REAL NOT NULL,
            FechaVenta REAL NOT NULL,
            FOREIGN KEY (Cliente_ID) REFERENCES cliente(Cliente_ID),
            FOREIGN KEY (Producto_ID) REFERENCES producto(Producto_ID)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicio_tecnico (
            Servicio_ID TEXT PRIMARY KEY,
            Cliente_ID TEXT NOT NULL,
            EquipoModelo TEXT NOT NULL,
            DescripcionFalla TEXT NOT NULL,
            CostoReparacion REAL NOT NULL,
            Estado TEXT NOT NULL,
            FechaIngreso TEXT NOT NULL,
            FechaEntrega TEXT NOT NULL,
            FOREIGN KEY (Cliente_ID) REFERENCES cliente(Cliente_ID)
        )
    """)
    
    conn.commit()
    conn.close()