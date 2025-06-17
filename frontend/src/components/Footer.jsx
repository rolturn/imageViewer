// src/components/Footer.js
import React from 'react';

const Footer = ({ page }) => {
  let footerText;

  switch(page) {
    case 'home':
      footerText = "Home Page Footer";
      break;
    case 'details':
      footerText = "Details Page Footer with Thumbnail Slider";
      break;
    default:
      footerText = "Default Footer";
  }

  return (
    <footer className="p-4 bg-gray-800 text-white">
      {footerText}
    </footer>
  );
};

export default Footer;