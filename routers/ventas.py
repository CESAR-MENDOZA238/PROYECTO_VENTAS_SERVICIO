from fastapi import APIRouter, HTTPException
from dao.venta_dao import VentaDAO, VentaNoEncontradaError
from dao.producto_dao import ProductoDAO
from dao.cliente_dao import ClienteDAO
from modelos.venta import Venta
from schemas.venta_schema import VentaCrear, VentaActualizar, VentaRespuesta

router = APIRouter(prefix="/ventas", tags=["Ventas"])
vdao = VentaDAO()
cdao = ClienteDAO()
pdao = ProductoDAO()

@router.get("", response_model=list[VentaRespuesta])
def listar_ventas():
    return vdao.obtener_todos()

@router.get("/{venta_id}", response_model=VentaRespuesta)
def obtener_venta(venta_id: int):
    v = vdao.buscar_por_id(venta_id)
    if not v:
        raise HTTPException(status_code=404, detail=f"Venta ID={venta_id} no encontrada")
    return v

# OJO: esta ruta va ANTES de /{venta_id} para que FastAPI no confunda
# "cliente" con un ID numérico.
@router.get("/cliente/{cliente_id}", response_model=list[VentaRespuesta])
def ventas_por_cliente(cliente_id: int):
    c = cdao.buscar_por_id(cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Cliente ID={cliente_id} no encontrado")
    return vdao.buscar_por_cliente(cliente_id)

@router.post("", response_model=VentaRespuesta, status_code=201)
def registrar_venta(datos: VentaCrear):
    c = cdao.buscar_por_id(datos.cliente_id)
    p = pdao.buscar(datos.producto_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Cliente ID={datos.cliente_id} no encontrado")
    if not p:
        raise HTTPException(status_code=404, detail=f"Producto ID={datos.producto_id} no encontrado")
    v = vdao.registrar(Venta(datos.cliente_id, datos.producto_id, datos.cantidad), p.precio)
    return vdao.buscar_por_id(v.id)

@router.put("/{venta_id}", response_model=VentaRespuesta)
def actualizar_venta(venta_id: int, datos: VentaActualizar):
    v = vdao.buscar_por_id(venta_id)
    if not v:
        raise HTTPException(status_code=404, detail=f"Venta ID={venta_id} no encontrada")
    p = pdao.buscar(v["producto_id"])
    try:
        return vdao.actualizar(venta_id, datos.cantidad, p.precio)
    except VentaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{venta_id}")
def eliminar_venta(venta_id: int):
    try:
        vdao.eliminar(venta_id)
        return {"mensaje": f"Venta ID={venta_id} eliminada"}
    except VentaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))