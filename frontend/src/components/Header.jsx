// src/components/Header.js
import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="p-4 bg-gray-800 text-white">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-lg font-bold">ImageViewer</h1>
        <nav>
          <ul className="flex space-x-4">
            <li><Link to="/" className="hover:underline">Home</Link></li>
            <li><Link to="/picks" className="hover:underline">Picks</Link></li>
            <li><Link to="/trash" className="hover:underline">Trash</Link></li>
            <li><Link to="/config" className="hover:underline">Config</Link></li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;