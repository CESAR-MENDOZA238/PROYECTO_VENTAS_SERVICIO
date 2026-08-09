class Cliente:
    def __init__(self, nombre, RUC, email, telefono):
        self.id             = None
        self.nombre         =nombre
        self.ruc            =RUC
        self.email          =email
        self.telefono       =telefono
    
    def __str__(self):
        return f"Cliente: {self.nombre}, RUC: {self.ruc}, Email: {self.email}, Teléfono: {self.telefono}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ruc": self.ruc,
            "email": self.email,
            "telefono": self.telefono
        }
        
@classmethod
def from_dict(cls, data):
        cliente = cls(
            nombre=data.get("nombre"),
            RUC=data.get("ruc"),
            email=data.get("email"),
            telefono=data.get("telefono")
        )
        cliente.id = data.get("id")
        return cliente
    
    
        
        
        
        