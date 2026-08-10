// src/Sidebar.jsx
import React, { useState } from 'react';
import { Nav, Button } from 'react-bootstrap';
import { 
  FaUser, 
  FaBox, 
  FaShoppingCart, 
  FaHeadset, 
  FaBars, 
  FaTools
} from 'react-icons/fa';
import logo from './assets/imagenes/api.png'


export function Sidebar({ activeOption, onSelectOption }) {
  const [collapsed, setCollapsed] = useState(false);

  const menuItems = [
    { key: 'clientes', label: 'Clientes', icon: <FaUser size={20} /> },
    { key: 'productos', label: 'Productos', icon: <FaBox size={20} /> },
    { key: 'ventas', label: 'Ventas', icon: <FaShoppingCart size={20} /> },
    { key: 'servicio', label: 'Servicio', icon: <FaTools size={20} /> },
  ];

  return (
    <div 
      className="d-flex flex-column flex-shrink-0 p-3 bg-dark text-white vh-100 position-sticky top-0"
      style={{ width: collapsed ? '80px' : '250px', transition: 'width 0.3s ease' }}
    >
      <div className="d-flex align-items-center justify-content-between mb-4">
        <img src={logo} alt="miLogo" className="img-fluid rounded shadow-sm w-25" />
        {!collapsed && <span className="fs-4 fw-bold">Servicio Técnico</span>}
        
        <Button variant="outline-light" size="sm" onClick={() => setCollapsed(!collapsed)} className="ms-auto">
          <FaBars  />

        </Button>
      </div>

      <hr className="my-2" />

      <Nav variant="pills" className="flex-column mb-auto">
        {menuItems.map((item) => (
          <Nav.Item key={item.key} className="mb-1">
            <Nav.Link 
              active={activeOption === item.key}
              onClick={() => onSelectOption(item.key)}
              className="text-white d-flex align-items-center gap-3 cursor-pointer"
              style={{ cursor: 'pointer' }}
            >
              {item.icon}
              {!collapsed && <span>{item.label}</span>}
            </Nav.Link>
          </Nav.Item>
        ))}
      </Nav>
    </div>
  );
}