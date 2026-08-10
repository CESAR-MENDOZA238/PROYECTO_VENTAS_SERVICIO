class Producto:
    def __init__(self, nombre, precio):
        self.id = None
        self.nombre = nombre
        self.precio = precio
    
    def __str__(self):
        return f"[{self.id}] {self.nombre} | S/.{self.precio:.2f}"
    
    def to_dict(self):
        
        return{
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio
        }
        
    @classmethod
    def from_dict(cls, datos):
        p = cls(datos["nombre"], datos["precio"])
        p.id = datos["id"]
        return p