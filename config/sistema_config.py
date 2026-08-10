from config.logger import Logger

class SistemaConfig:
    _inst = None              # Guarda la única instancia

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
            cls._inst.nombre  = "Ventas ServiciosPOO"  # Nombre del sistema
            cls._inst.version = "1.1"                     # Versión
            cls._inst.empresa = "IESTP Argentina"         # Empresa
            cls._inst.autor   = "Cesar Mendoza, Edwin Flores"          # Autor
            Logger().info(
                f"Sistema Iniciado : {cls._inst.nombre}"
                f"Version : {cls._inst.version}"
                f"Empresa : {cls._inst.empresa}"
                f"Autor : {cls._inst.autor}"
            )
            return cls._inst

class ClienteNoEncontradoError(Exception):
    def __init__(self, id):
        super().__init__(f"Cliente ID = {id} no encontrado")
        # super().__init__() llama al constructor de Exception
        # con nuestro mensaje personalizado

class RUCDuplicadoError(Exception):
    def __init__(self, ruc):
        super().__init__(f"RUC '{ruc}' ya registrado")