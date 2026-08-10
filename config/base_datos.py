import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env (ubicado en la raíz del backend)
load_dotenv()


def obtener_conexion():
    # 1. Obtenemos los valores de conexión desde las variables de entorno (.env)
    host = os.getenv("BD_HOST", "localhost")
    port = os.getenv("BD_PORT", "5432")
    user = os.getenv("BD_USER", "postgres")

    # IMPORTANTE: Coloca tu contraseña real en el archivo .env
    password = os.getenv("BD_PASSWORD", "135421")

    # Nombre de la base de datos creada a partir de BD_VENTAS_SERVICIO.sql
    database = os.getenv("BD_NAME", "bd_ventas_servicio")

    # 2. Conexión mediante URI
    database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    # cursor_factory=RealDictCursor permite acceder a las columnas por nombre
    # (fila["nombre"], fila["id"], etc.) en lugar de por índice numérico.
    conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
    return conn


def inicializar():
    # Crea las tablas si aún no existen. Se llama UNA vez al iniciar el sistema.
    # "IF NOT EXISTS" evita un error si la tabla ya fue creada en una ejecución anterior.
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Tabla de clientes: ruc tiene restricción UNIQUE para evitar duplicados a nivel de BD.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
        id          SERIAL  PRIMARY KEY,
        nombre      TEXT    NOT NULL,
        ruc         TEXT    UNIQUE NOT NULL,
        email       TEXT    NOT NULL,
        telefono    TEXT    NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL
        )
    """)

    # Tabla de ventas: tiene FOREIGN KEY que enlaza con clientes y productos.
    # FOREIGN KEY garantiza integridad referencial: no se puede registrar una venta
    # con un cliente_id o producto_id que no exista en sus tablas respectivas.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id          SERIAL          PRIMARY KEY,
            cliente_id  INTEGER         NOT NULL,
            producto_id INTEGER         NOT NULL,
            cantidad    INTEGER         NOT NULL,
            fecha       TEXT            NOT NULL,
            total       NUMERIC(10,2)   NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)

    # Tabla de servicios (soporte técnico): módulo nuevo requerido por el
    # frontend VentaServicio (vista "Servicio").
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id                SERIAL          PRIMARY KEY,
            cliente_id        INTEGER         NOT NULL,
            equipo_modelo     TEXT            NOT NULL,
            descripcion_falla TEXT            NOT NULL,
            costo_reparacion  NUMERIC(10,2)   NOT NULL DEFAULT 0,
            estado            TEXT            NOT NULL DEFAULT 'Pendiente',
            fecha_ingreso     TEXT            NOT NULL,
            fecha_entrega     TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    # conn.commit() confirma todos los cambios (equivale a "guardar" en la BD).
    # Sin commit(), los cambios se pierden al cerrar la conexión.
    conn.commit()
    conn.close()
