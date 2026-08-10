-- ============================================================
-- BD_VENTAS_SERVICIO.sql
-- Script de creación de la base de datos y sus tablas.
--
-- El backend (config/base_datos.py -> inicializar()) crea las
-- tablas automáticamente la primera vez que se ejecuta, así que
-- este script es OPCIONAL: úsalo solo si prefieres crear la
-- base de datos y las tablas manualmente desde pgAdmin / psql.
-- ============================================================

-- 1) Crear la base de datos (ejecutar conectado a "postgres")
-- NOTA: LC_COLLATE/LC_CTYPE 'Spanish_Peru.1252' es un locale de Windows.
-- En Linux/Mac usa 'C.UTF-8' o el locale español disponible en tu sistema
-- (ej. 'es_PE.UTF-8'), o simplemente omite esas líneas para usar el
-- locale por defecto del servidor.

-- DROP DATABASE IF EXISTS bd_ventas_servicio;

CREATE DATABASE bd_ventas_servicio
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    TEMPLATE = template0
    -- En Windows puedes usar:
    -- LC_COLLATE = 'Spanish_Peru.1252'
    -- LC_CTYPE = 'Spanish_Peru.1252'
    -- En Linux/Mac:
    LC_COLLATE = 'C.UTF-8'
    LC_CTYPE = 'C.UTF-8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- 2) Conéctate a bd_ventas_servicio antes de ejecutar lo siguiente
-- (en psql: \c bd_ventas_servicio)

CREATE TABLE IF NOT EXISTS clientes (
    id          SERIAL  PRIMARY KEY,
    nombre      TEXT    NOT NULL,
    ruc         TEXT    UNIQUE NOT NULL,
    email       TEXT    NOT NULL,
    telefono    TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id      SERIAL PRIMARY KEY,
    nombre  TEXT   NOT NULL,
    precio  REAL   NOT NULL
);

CREATE TABLE IF NOT EXISTS ventas (
    id          SERIAL          PRIMARY KEY,
    cliente_id  INTEGER         NOT NULL,
    producto_id INTEGER         NOT NULL,
    cantidad    INTEGER         NOT NULL,
    fecha       TEXT            NOT NULL,
    total       NUMERIC(10,2)   NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

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
);
