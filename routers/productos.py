from fastapi import APIRouter, HTTPException
from dao.producto_dao import ProductoDAO, ProductoNoEncontradoError
from modelos.producto import Producto
from schemas.producto_schema import ProductoCrear, ProductoActualizar, ProductoRespuesta

router = APIRouter(prefix="/productos", tags=["Productos"])
dao = ProductoDAO()

@router.get("", response_model=list[ProductoRespuesta])
def listar_productos():
    return [p.to_dict() for p in dao.obtener_todos()]

@router.get("/{prod_id}", response_model=ProductoRespuesta)
def obtener_producto(prod_id: int):
    p = dao.buscar(prod_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Producto ID={prod_id} no encontrado")
    return p.to_dict()

@router.post("", response_model=ProductoRespuesta, status_code=201)
def crear_producto(datos: ProductoCrear):
    p = dao.insertar(Producto(datos.nombre, datos.precio))
    return p.to_dict()

@router.put("/{prod_id}", response_model=ProductoRespuesta)
def actualizar_producto(prod_id: int, datos: ProductoActualizar):
    try:
        p = dao.actualizar(prod_id, datos.nombre, datos.precio)
        return p.to_dict()
    except ProductoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))

@router.delete("/{prod_id}")
def eliminar_producto(prod_id: int):
    try:
        dao.eliminar(prod_id)
        return {"mensaje": f"Producto ID={prod_id} eliminado"}
    except ProductoNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))