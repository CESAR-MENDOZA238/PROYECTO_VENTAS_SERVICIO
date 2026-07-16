class ServicioTecnico:
    def __init__(self, Cliente, EquipoModelo, DescripcionFalla, CostoReparacion, Estado,FechaIngreso, FechaEntrega):
        self.id = None
        self.cliente = Cliente
        self.equipoModelo = EquipoModelo
        self.descripcionFalla = DescripcionFalla
        self.CostoReparacion = CostoReparacion
        self.estado = Estado
        self.FechaIngreso = FechaIngreso
        self.FechaEntrega = FechaEntrega
        