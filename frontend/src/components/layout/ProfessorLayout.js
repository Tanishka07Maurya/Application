import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

export default function ProfessorLayout() {
  return (
    <div className="dashboard-layout">
      <Sidebar />
      {/* Outlet will render the specific professor page (Dashboard, Results, etc.) */}
      <Outlet />
    </div>
  );
}