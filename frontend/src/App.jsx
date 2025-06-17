// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Homepage from './pages/Homepage';
import DetailsPage from './pages/DetailsPage';
import TrashPage from './pages/TrashPage';
import PicksPage from './pages/PicksPage';
import AuthenticationPage from './pages/AuthenticationPage';
import SettingsPage from './pages/SettingsPage';
import Header from './components/Header'; // Import the Header component
import Footer from './components/Footer'; // Import the Footer component

function App() {
  return (
    <Router>
      <div className="App">
        <Header /> {/* Add the Header component */}
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/details/:id" element={<DetailsPage />} />
          <Route path="/trash" element={<TrashPage />} />
          <Route path="/picks" element={<PicksPage />} />
          <Route path="/auth" element={<AuthenticationPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
        <Footer /> {/* Add the Footer component */}
      </div>
    </Router>
  );
}

export default App;