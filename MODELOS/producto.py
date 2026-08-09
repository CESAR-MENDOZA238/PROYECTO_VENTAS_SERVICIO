class Producto:
    def __init__(self, Nombre,Precio):
        self.id = None
        self.nombre = Nombre
        self.precio = Precio
        
    def __str__(self):
        return f"Producto: {self.nombre}, Precio: {self.precio}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio
        }
        
@classmethod
def from_dict(cls, data):
        producto = cls(
            Nombre=data.get("nombre"),
            Precio=data.get("precio")
        )
        producto.id = data.get("id")
        return producto
    
            
