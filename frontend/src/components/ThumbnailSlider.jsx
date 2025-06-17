// src/components/ThumbnailSlider.js
import React from 'react';

const ThumbnailSlider = ({ images, onSelect }) => {
  return (
    <div className="flex space-x-2 overflow-auto">
      {images.map(image => (
        <img key={image.id} src={image.src} alt={image.name}
          className="w-16 h-16 cursor-pointer" onClick={() => onSelect(image.id)} />
      ))}
    </div>
  );
};

export default ThumbnailSlider;