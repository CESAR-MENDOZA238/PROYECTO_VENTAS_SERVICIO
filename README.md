# 🛒 Sistema de Gestor de Ventas y Servicio Técnico

Un sistema web completo e integral para la gestión comercial y soporte técnico, diseñado para optimizar el control de clientes, catálogo de productos con gestión de inventario, registro de ventas y seguimiento pormenorizado de órdenes de reparación y servicio técnico.

El proyecto está construido bajo una arquitectura desacoplada moderna, rápida y escalable: **FastAPI** en el backend, **React** con **Bootstrap 5** en el frontend, y **Microsoft SQL Server** como motor de base de datos relacional.

---

## 📸 Vista Previa e Interfaz
*(Sugerencia: Incluye capturas de pantalla de la aplicación aquí)*

| Módulo de Ventas | Seguimiento de Servicio Técnico |
| :---: | :---: |
| ![Ventas](https://via.placeholder.com/400x220?text=Modulo+Ventas) | ![Servicio Tecnico](https://via.placeholder.com/400x220?text=Servicio+Tecnico) |

---

## 🛠️ Tecnologías Utilizadas

### **Backend**
* **Python 3.10+**: Lenguaje de programación principal.
* **FastAPI**: Framework web asíncrono de alto rendimiento y bajo overhead.
* **Uvicorn**: Servidor ASGI rápido para producción y desarrollo.
* **SQLAlchemy**: ORM (Object-Relational Mapping) para una interacción fluida con SQL Server.
* **Pydantic**: Validación y serialización estricta de esquemas de datos.

### **Frontend**
* **React**: Librería de JavaScript para construir interfaces de usuario modulares y reactivas.
* **Bootstrap 5 / React-Bootstrap**: Estilos responsivos, componentes de UI estilizados e íconos.
* **Axios**: Cliente HTTP para interactuar con la API REST de FastAPI.
* **React Router DOM**: Enrutamiento del lado del cliente.

### **Base de Datos**
* **Microsoft SQL Server**: Sistema de gestión de bases de datos relacionales (RDBMS).

---

## 🗄️ Modelo de Base de Datos (`BD_VENTAS_SERVICIO`)

La arquitectura de datos está diseñada relacionalmente para mantener la integridad referencial y garantizar restricciones de negocio directamente en la base de datos:

1. **`Clientes`**: Almacena información de contacto de los usuarios/compradores (ID, Nombre, Teléfono, Email único, Dirección, Fecha de Registro).
2. **`Productos`**: Catálogo comercial con validación de stock no negativo (`Stock >= 0`).
3. **`Ventas`**: Registro de transacciones con control de cantidad vendida (`Cantidad > 0`) e integridad referencial vinculada a clientes y productos.
4. **`ServicioTecnico`**: Gestión detallada de reparaciones de equipos (Modelo, Falla, Costo, Fechas de ingreso/entrega) con flujo restringido de estados:
   * 📥 `Recibido`
   * 🔍 `En Diagnostico`
   * 🛠️ `En Reparacion`
   * ✅ `Listo`
   * 📦 `Entregado`

---

## 📁 Estructura del Proyecto

```text
BD_VENTAS_SERVICIO/
├── backend/
│   ├── app/
│   │   ├── api/             # Endpoints / Rutas (Clientes, Productos, Ventas, Servicios)
│   │   ├── core/            # Configuración general y variables de entorno
│   │   ├── db/              # Conexión a la base de datos y sesión de SQLAlchemy
│   │   ├── models/          # Modelos de SQLAlchemy
│   │   ├── schemas/         # Esquemas de Pydantic
│   │   └── main.py          # Punto de entrada de la API
│   ├── requirements.txt     # Dependencias de Python
│   └── .env.example         # Plantilla de variables de entorno
│
├── frontend/
│   ├── public/              # Archivos estáticos
│   ├── src/
│   │   ├── components/      # Componentes reutilizables (Navbar, Cards, Modales)
│   │   ├── pages/           # Vistas principales (Clientes, Productos, Ventas, Servicio)
│   │   ├── services/        # Servicios de integración con Axios
│   │   ├── App.js           # Configuración de rutas
│   │   └── index.js         # Punto de entrada de React
│   ├── package.json         # Dependencias de Node.js
│   └── README.md
│
└── database/
    └── BD_VENTAS_SERVICIO.sql  # Script de creación de BD, tablas y datos iniciales
```

---

## 🚀 Instalación y Configuración Paso a Paso

### **Prerrequisitos**
* [Python 3.10+](https://www.python.org/)
* [Node.js (v16+) y npm](https://nodejs.org/)
* [SQL Server Management Studio (SSMS)](https://docs.microsoft.com/sql/ssms/download-sql-server-management-studio-ssms) o [Azure Data Studio](https://azure.microsoft.com/services/developer-tools/azure-data-studio/)

---

### **1. Configuración de la Base de Datos**

1. Abre tu gestor de SQL Server (SSMS o Azure Data Studio).
2. Ejecuta el archivo SQL ubicado en `database/BD_VENTAS_SERVICIO.sql`.
   
   *El script creará la base de datos, las tablas con sus respectivas restricciones (`CHECK`, `FOREIGN KEY`) e insertará registros de prueba.*

---

### **2. Configuración del Backend (FastAPI)**

1. Navega al directorio del backend:
   ```bash
   cd backend
   ```

2. Crea y activa un entorno virtual de Python:
   * **En Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * **En Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   Crea un archivo `.env` en la carpeta `backend/` basándote en `.env.example`:
   ```env
   DATABASE_URL=mssql+pyodbc://tu_usuario:tu_password@localhost/BD_VENTAS_SERVICIO?driver=ODBC+Driver+17+for+SQL+Server
   ```

5. Inicia el servidor de desarrollo de FastAPI:
   ```bash
   uvicorn main:app --reload
   ```

   * **API Base:** `http://127.0.0.1:8000`
   * **Documentación interactiva Swagger:** `http://127.0.0.1:8000/docs`
   * **Documentación Redoc:** `http://127.0.0.1:8000/redoc`

---

### **3. Configuración del Frontend (React + Bootstrap)**

1. Navega a la carpeta del frontend:
   ```bash
   cd ../frontend
   ```

2. Instala las dependencias del proyecto:
   ```bash
   npm install
   ```

3. Inicia la aplicación en modo desarrollo:
   ```bash
   npm start
   ```

   La aplicación estará corriendo automáticamente en `http://localhost:3000`.

---

## 📡 Endpoints de la API

La API cuenta con documentación autogenerada disponible en `/docs`. A continuación se detallan los endpoints principales:

### 👤 **Clientes (`/api/clientes`)**
* `GET /api/clientes/` - Listar todos los clientes.
* `POST /api/clientes/` - Registrar un nuevo cliente.
* `GET /api/clientes/{id}` - Obtener detalles de un cliente específico.
* `PUT /api/clientes/{id}` - Actualizar información del cliente.

### 📦 **Productos (`/api/productos`)**
* `GET /api/productos/` - Consultar inventario y catálogo de productos.
* `POST /api/productos/` - Agregar un nuevo producto al stock.
* `PUT /api/productos/{id}` - Actualizar precio o stock del producto.

### 💰 **Ventas (`/api/ventas`)**
* `GET /api/ventas/` - Historial completo de ventas registradas.
* `POST /api/ventas/` - Registrar nueva venta (descuenta automáticamente del stock).

### 🔧 **Servicio Técnico (`/api/servicio-tecnico`)**
* `GET /api/servicio-tecnico/` - Listar todas las órdenes de soporte técnico.
* `POST /api/servicio-tecnico/` - Crear una nueva orden para un cliente.
* `PATCH /api/servicio-tecnico/{id}/estado` - Cambiar estado (`Recibido` ➡️ `En Diagnostico` ➡️ `En Reparacion` ➡️ `Listo` ➡️ `Entregado`).

---

## 🤝 Contribución

1. Haz un **Fork** del proyecto.
2. Crea una rama para tu nueva característica (`git checkout -b feature/NuevaCaracteristica`).
3. Guarda tus cambios (`git commit -m 'Añade una nueva característica'`).
4. Haz Push a la rama (`git push origin feature/NuevaCaracteristica`).
5. Abre un **Pull Request**.

---

## 📝 Licencia

Este proyecto se distribuye bajo la licencia **MIT**. Para más detalles, consulta el archivo `LICENSE`.
