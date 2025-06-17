// src/components/ImageSidebar.js
import React from 'react';

const ImageSidebar = ({ image, onNavigate, onRate, onAddNotes, onAddPrompt }) => {
  return (
    <div className="p-4 bg-gray-200 w-1/4">
      <h2>Filename: {image.name}</h2>
      <div className="flex justify-between mb-4">
        <button onClick={() => onNavigate('prev')}>❮</button>
        <button onClick={() => onNavigate('next')}>❯</button>
      </div>
      {[1, 2, 3, 4].map(rating => (
        <button key={rating} onClick={() => onRate(image.id, rating)}>{rating}</button>
      ))}
      <textarea
        placeholder="Notes"
        className="block w-full mt-2 p-2 border"
        onChange={(e) => onAddNotes(image.id, e.target.value)}
      />
      <textarea
        placeholder="Prompt"
        className="block w-full mt-2 p-2 border"
        onChange={(e) => onAddPrompt(image.id, e.target.value)}
      />
    </div>
  );
};

export default ImageSidebar;