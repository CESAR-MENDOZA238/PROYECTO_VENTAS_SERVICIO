// src/App.jsx
import React, { useState } from 'react';
import { Sidebar } from './Sidebar';
import { ClientesView, ProductosView, VentasView, ServicioView } from './views/Modulos';

export default function App() {
  const [activeTab, setActiveTab] = useState('clientes');

  const renderContent = () => {
    switch (activeTab) {
      case 'clientes':
        return <ClientesView />;
      case 'productos':
        return <ProductosView />;
      case 'ventas':
        return <VentasView />;
      case 'servicio':
        return <ServicioView />;
      default:
        return <ClientesView />;
    }
  };

  return (
    <div className="d-flex bg-light min-vh-100">
      <Sidebar activeOption={activeTab} onSelectOption={setActiveTab} />
      <main className="flex-grow-1 overflow-auto">
        {renderContent()}
      </main>
    </div>
  );
}