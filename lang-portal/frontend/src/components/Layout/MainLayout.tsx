// src/components/Layout/MainLayout.tsx
import React from 'react';
import Navbar from '../Navigation/Navbar';
import { Outlet } from 'react-router-dom';
import { useTheme } from '../../contexts/ThemeContext';

const MainLayout: React.FC = () => {
  const { isDark } = useTheme();

  return (
    <div className={`min-h-screen flex flex-col ${isDark ? 'bg-gray-900' : 'bg-gray-50'}`}>
      <Navbar />
      <main className="flex-grow flex justify-center">
        <div className="w-full max-w-7xl px-4 sm:px-6 lg:px-8 py-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default MainLayout;
