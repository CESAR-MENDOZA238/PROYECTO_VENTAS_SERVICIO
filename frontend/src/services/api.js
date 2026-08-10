// src/services/api.js
// URL del backend FastAPI (Semana14PostgreSQL). Se puede sobreescribir
// creando un archivo .env en la raíz del frontend con:
//   VITE_API_URL=http://localhost:8000
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function apiFetch(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': `Bearer ${localStorage.getItem('token')}` // Si requieres token
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  // Los endpoints del backend FastAPI usan barra final (/clientes/, /productos/, etc.)
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, options);

    // Para respuestas DELETE o respuestas sin contenido (204)
    if (response.status === 204 || (response.status === 200 && response.headers.get('content-length') === '0')) {
      return { success: true };
    }

    if (!response.ok) {
      let detalle = response.statusText;
      try {
        const data = await response.json();
        detalle = data.detail || detalle;
      } catch (_) {
        // el cuerpo no era JSON, se mantiene el statusText
      }
      throw new Error(`Error ${response.status}: ${detalle}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Error en petición ${method} ${url}:`, error);
    throw error;
  }
}
