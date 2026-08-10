// src/components/ModuloCrud.jsx
import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Spinner, Alert } from 'react-bootstrap';
import { FaPlus, FaEdit, FaTrash } from 'react-icons/fa';
import { apiFetch } from '../services/api';

export function ModuloCrud({ titulo, endpoint, campos }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para Modal (Crear / Editar)
  const [showModal, setShowModal] = useState(false);
  const [editItem, setEditItem] = useState(null); // null = Crear, Objeto = Editar
  const [formData, setFormData] = useState({});

  // 1. GET: Cargar datos desde la API
  const cargarDatos = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch(endpoint, 'GET');
      setItems(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(`No se pudieron cargar los datos de ${titulo.toLowerCase()}.`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarDatos();
  }, [endpoint]);

  // Manejadores de Modal
  // Nota: algunos campos muestran en la tabla un valor "legible" (col.key,
  // p.ej. el nombre del cliente) pero el formulario debe enviar el valor
  // real que espera la API (col.editKey, p.ej. cliente_id). Si no se define
  // editKey, se usa key para ambos casos.
  const handleOpenModal = (item = null) => {
    setEditItem(item);
    if (item) {
      const datosForm = {};
      campos.forEach((col) => {
        const campoForm = col.editKey || col.key;
        datosForm[campoForm] = item[campoForm] ?? '';
      });
      setFormData(datosForm);
    } else {
      // Inicializar campos vacíos
      const inicial = {};
      campos.forEach((col) => (inicial[col.editKey || col.key] = ''));
      setFormData(inicial);
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditItem(null);
    setFormData({});
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // 2. POST / PUT: Guardar cambios
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editItem) {
        // PUT
        await apiFetch(`${endpoint}/${editItem.id}`, 'PUT', formData);
      } else {
        // POST
        await apiFetch(endpoint, 'POST', formData);
      }
      handleCloseModal();
      cargarDatos(); // Recargar la lista
    } catch (err) {
      alert(`Error al guardar en ${titulo}`);
    }
  };

  // 3. DELETE: Eliminar elemento
  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar este registro?')) {
      try {
        await apiFetch(`${endpoint}/${id}`, 'DELETE');
        cargarDatos(); // Recargar la lista
      } catch (err) {
        alert('Error al intentar eliminar el registro.');
      }
    }
  };

  return (
    <div className="container-fluid p-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold m-0">{titulo}</h2>
          <p className="text-muted m-0">Gestión de registros vía API REST</p>
        </div>
        <Button variant="primary" onClick={() => handleOpenModal()}>
          <FaPlus className="me-2" /> Nuevo Registro
        </Button>
      </div>

      {error && <Alert variant="danger">{error}</Alert>}

      {loading ? (
        <div className="text-center py-5">
          <Spinner animation="border" variant="primary" />
          <p className="mt-2 text-muted">Cargando datos...</p>
        </div>
      ) : (
        <div className="card border-0 shadow-sm">
          <div className="card-body p-0">
            <Table responsive hover className="align-middle mb-0">
              <thead className="bg-light">
                <tr>
                  <th>ID</th>
                  {campos.map((col) => (
                    <th key={col.key}>{col.label}</th>
                  ))}
                  <th className="text-end">Acciones</th>
                </tr>
              </thead>
              <tbody>
                {items.length === 0 ? (
                  <tr>
                    <td colSpan={campos.length + 2} className="text-center py-4 text-muted">
                      No hay registros disponibles.
                    </td>
                  </tr>
                ) : (
                  items.map((item) => (
                    <tr key={item.id}>
                      <td className="fw-semibold">#{item.id}</td>
                      {campos.map((col) => (
                        <td key={col.key}>{item[col.key]}</td>
                      ))}
                      <td className="text-end">
                        <Button
                          variant="outline-warning"
                          size="sm"
                          className="me-2"
                          onClick={() => handleOpenModal(item)}
                        >
                          <FaEdit />
                        </Button>
                        <Button
                          variant="outline-danger"
                          size="sm"
                          onClick={() => handleDelete(item.id)}
                        >
                          <FaTrash />
                        </Button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </Table>
          </div>
        </div>
      )}

      {/* Modal para Crear y Editar */}
      <Modal show={showModal} onHide={handleCloseModal} centered>
        <Form onSubmit={handleSubmit}>
          <Modal.Header closeButton>
            <Modal.Title>{editItem ? `Editar en ${titulo}` : `Nuevo en ${titulo}`}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {campos.map((col) => {
              const campoForm = col.editKey || col.key;
              return (
                <Form.Group className="mb-3" key={campoForm}>
                  <Form.Label>{col.editLabel || col.label}</Form.Label>
                  <Form.Control
                    type={col.type || 'text'}
                    name={campoForm}
                    value={formData[campoForm] || ''}
                    onChange={handleInputChange}
                    required={col.required !== false}
                  />
                </Form.Group>
              );
            })}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleCloseModal}>
              Cancelar
            </Button>
            <Button variant="primary" type="submit">
              {editItem ? 'Actualizar (PUT)' : 'Guardar (POST)'}
            </Button>
          </Modal.Footer>
        </Form>
      </Modal>
    </div>
  );
}