class Venta:
    def __init__(self, Cliente, Producto, Cantidad, Total, Fecha):
        self.id = None
        self.cliente = Cliente
        self.producto = Producto
        self.cantidad = Cantidad
        self.totalVenta = Total
        self.fechaVenta = Fecha
        
    def __str__(self):
        return f"Venta: Cliente: {self.cliente}, Producto: {self.producto}, Cantidad: {self.cantidad}, Total: {self.total}, Fecha: {self.fecha}"  
    
    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.cliente.to_dict() if self.cliente else None,
            "producto": self.producto.to_dict() if self.producto else None,
            "cantidad": self.cantidad,
            "totalVenta": self.totalVenta,
            "fechaVenta": self.fechaVenta
        }
        
    @classmethod
    def from_dict(cls, data):
        cliente_data = data.get("cliente")
        producto_data = data.get("producto")
        
        cliente = cliente.from_dict(cliente_data) if cliente_data else None
        producto = producto.from_dict(producto_data) if producto_data else None
        
        venta = cls(
            Cliente=cliente,
            Producto=producto,
            Cantidad=data.get("cantidad"),
            Total=data.get("totalVenta"),
            Fecha=data.get("fechaVenta")
        )
        venta.id = data.get("id")
        return venta    
    
