// src/pages/Homepage.js
import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import ImageCard from '../components/ImageCard';

const Homepage = () => {
  const [images] = useState([
    { id: 1, name: 'Image 1', src: '/images/ComfyUI_00001_.png' },
    // Add more images as needed
  ]);

  const handleTrash = (id) => {
    console.log(`Trashing image ${id}`);
  };

  const handleRate = (id, rating) => {
    console.log(`Rating image ${id} with ${rating}`);
  };

  const handlePick = (id) => {
    console.log(`Picking image ${id}`);
  };

  return (
    <>
      <Header />
      <main className="container mx-auto p-4">
        <div className="grid grid-cols-3 gap-4">
          {images.map(image => (
            <ImageCard key={image.id} image={image}
              onTrash={handleTrash}
              onRate={handleRate}
              onPick={handlePick}
            />
          ))}
        </div>
      </main>
      <Footer page="home" />
    </>
  );
};

export default Homepage;