class Venta:
    def __init__(self, Cliente, Producto, Cantidad, TotalVenta, FechaVenta):
        self.id = None
        self.cliente = Cliente
        self.producto = Producto
        self.cantidad = Cantidad
        self.totalVenta = TotalVenta
        self.fechaVenta = FechaVenta