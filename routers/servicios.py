from fastapi import APIRouter, HTTPException
from dao.servicio_dao import ServicioDAO, ServicioNoEncontradoError
from dao.cliente_dao import ClienteDAO
from modelos.servicio import Servicio
from schemas.servicio_schema import ServicioCrear, ServicioActualizar, ServicioRespuesta

router = APIRouter(prefix="/servicios", tags=["Servicios"])
dao = ServicioDAO()
cdao = ClienteDAO()


@router.get("", response_model=list[ServicioRespuesta])
def listar_servicios():
    return dao.obtener_todos()


@router.get("/{servicio_id}", response_model=ServicioRespuesta)
def obtener_servicio(servicio_id: int):
    s = dao.buscar_por_id(servicio_id)
    if not s:
        raise HTTPException(status_code=404, detail=f"Servicio ID={servicio_id} no encontrado")
    return s


@router.get("/cliente/{cliente_id}", response_model=list[ServicioRespuesta])
def servicios_por_cliente(cliente_id: int):
    c = cdao.buscar_por_id(cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Cliente ID={cliente_id} no encontrado")
    return [s for s in dao.obtener_todos() if s["cliente_id"] == cliente_id]


@router.post("", response_model=ServicioRespuesta, status_code=201)
def crear_servicio(datos: ServicioCrear):
    c = cdao.buscar_por_id(datos.cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Cliente ID={datos.cliente_id} no encontrado")
    s = Servicio(
        cliente_id=datos.cliente_id,
        equipo_modelo=datos.equipoModelo,
        descripcion_falla=datos.descripcionFalla,
        costo_reparacion=datos.costoReparacion,
        estado=datos.estado,
        fecha_entrega=datos.fechaEntrega,
    )
    creado = dao.registrar(s)
    return dao.buscar_por_id(creado.id)


@router.put("/{servicio_id}", response_model=ServicioRespuesta)
def actualizar_servicio(servicio_id: int, datos: ServicioActualizar):
    try:
        return dao.actualizar(
            servicio_id,
            equipo_modelo=datos.equipoModelo,
            descripcion_falla=datos.descripcionFalla,
            costo_reparacion=datos.costoReparacion,
            estado=datos.estado,
            fecha_entrega=datos.fechaEntrega,
        )
    except ServicioNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.delete("/{servicio_id}")
def eliminar_servicio(servicio_id: int):
    try:
        dao.eliminar(servicio_id)
        return {"mensaje": f"Servicio ID={servicio_id} eliminado"}
    except ServicioNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
