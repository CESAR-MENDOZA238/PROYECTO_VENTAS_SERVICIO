// src/views/Modulos.jsx
import React from 'react';
import { ModuloCrud } from '../components/ModuloCrud';

// 1. Clientes
export function ClientesView() {
  const campos = [
    { key: 'nombre', label: 'Nombre' },
    { key: 'ruc', label: 'RUC' },
    { key: 'email', label: 'Email', type: 'email' },
    { key: 'telefono', label: 'Teléfono' },
  ];
  return <ModuloCrud titulo="Clientes" endpoint="/clientes" campos={campos} />;
}

// 2. Productos
export function ProductosView() {
  const campos = [
    { key: 'nombre', label: 'Producto' },
    { key: 'precio', label: 'Precio (S/.)', type: 'number' },
  ];
  return <ModuloCrud titulo="Productos" endpoint="/productos" campos={campos} />;
}

// 3. Ventas
// La API (VentaRespuesta) devuelve tanto el nombre (cliente, producto) como
// el id (cliente_id, producto_id). En la tabla se muestra el nombre; en el
// formulario de creación se pide el id (editKey), ya que es lo que espera
// VentaCrear en el backend.
export function VentasView() {
  const campos = [
    { key: 'cliente', editKey: 'cliente_id', label: 'Cliente', editLabel: 'ID Cliente', type: 'number' },
    { key: 'producto', editKey: 'producto_id', label: 'Producto', editLabel: 'ID Producto', type: 'number' },
    { key: 'cantidad', label: 'Cantidad', type: 'number' },
    { key: 'total', label: 'Total', type: 'number', required: false },
    { key: 'fecha', label: 'Fecha', required: false },
  ];
  return <ModuloCrud titulo="Ventas" endpoint="/ventas" campos={campos} />;
}

// 4. Servicio (Soporte técnico)
export function ServicioView() {
  const campos = [
    { key: 'cliente', editKey: 'cliente_id', label: 'Cliente', editLabel: 'ID Cliente', type: 'number' },
    { key: 'equipoModelo', label: 'Equipo / Modelo' },
    { key: 'descripcionFalla', label: 'Descripción de la falla' },
    { key: 'costoReparacion', label: 'Costo de reparación (S/.)', type: 'number' },
    { key: 'estado', label: 'Estado' },
    { key: 'fechaIngreso', label: 'Fecha de ingreso', type: 'date', required: false },
    { key: 'fechaEntrega', label: 'Fecha de entrega', type: 'date', required: false },
  ];
  return <ModuloCrud titulo="Servicio" endpoint="/servicios" campos={campos} />;
}
