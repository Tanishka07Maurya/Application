import React from 'react';
import { Outlet } from 'react-router-dom'; // 👈 IMPORT THIS
import Sidebar from './Sidebar'; 
import Header from './Header'; 
import Footer from './Footer';

const ProfessorLayout = () => {
    return (
        <div className="layout-container" style={{ display: 'flex', minHeight: '100vh' }}>
            {/* 1. Sidebar on the left */}
            <Sidebar />

            <div className="main-content-wrapper" style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
                {/* 2. Header at the top */}
                <Header role="Professor" />

                {/* 3. DYNAMIC CONTENT HERE */}
                <div style={{ flex: 1, padding: '20px', backgroundColor: '#f4f6f8' }}>
                    <Outlet />  {/* 👈 THIS IS REQUIRED TO RENDER CHILD PAGES */}
                </div>

                {/* 4. Footer at the bottom */}
                <Footer />
            </div>
        </div>
    );
};

export default ProfessorLayout;