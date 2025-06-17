// src/components/ImageCard.js
import React from 'react';

const ImageCard = ({ image, onTrash, onRate, onPick }) => {
  return (
    <div className="relative">
      <img src={image.src} alt={image.name} className="w-full h-auto" />
      <div className="flex justify-around mt-2">
        <button onClick={() => onTrash(image.id)}>X</button>
        {[1, 2, 3, 4].map(rating => (
          <button key={rating} onClick={() => onRate(image.id, rating)}>{rating}</button>
        ))}
        <button onClick={() => onPick(image.id)}>✔️</button>
      </div>
    </div>
  );
};

export default ImageCard;