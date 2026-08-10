class Cliente():
    def __init__(self, nombre, ruc, email, telefono):
        self.id       = None      # El DAO asignará el ID al insertar
        self.nombre   = nombre    # Nombre completo o razón social
        self.ruc      = ruc       # Número de RUC (identificador único)
        self.email    = email     # Correo electrónico
        self.telefono = telefono  # Número de teléfono

    def __str__(self):
        # Controla cómo se muestra el objeto cuando hacemos print(cliente)
        return f"[{self.id}] {self.nombre} | RUC:{self.ruc} | {self.email}"
    
    def to_dict(self):
        
        return{
            "id": self.id,
            "nombre": self.nombre,
            "ruc": self.ruc,
            "email": self.email,
            "telefono": self.telefono
        }
        
    @classmethod
    def from_dict(cls, datos):
        c = cls(datos["nombre"], datos["ruc"], datos["email"], datos["telefono"])
        c.id = datos["id"]
        return c