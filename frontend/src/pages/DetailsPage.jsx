import React from 'react';
import { useParams } from 'react-router-dom';

function DetailsPage() {
  const { id } = useParams(); // Get the ID parameter from the URL

  return (
    <div>
      <h1>Details Page</h1>
      <p>This is the details page for image ID: {id}</p>
    </div>
  );
}

export default DetailsPage;