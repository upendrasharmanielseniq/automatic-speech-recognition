import React, { useState } from 'react';
import { predictFromSlidingWindow } from '../services/api';

const SlidingWindow = () => {
    const [file, setFile] = useState([]);

    const handleChange = (e) => {
        setFile(e.target.files[0]);  
    }
    
   const handleUpload = async () => {
    if (!file) {
        alert("Please select a file first.");
        return;
    }

    try {
        const response = await predictFromSlidingWindow(file);
        const blob = new Blob([response.data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'Sliding_Window_Predictions.csv';
        link.click();
    } catch (error) {
        console.error('Error uploading file:', error);
        alert('Failed to upload file. Please try again.');
    }
};

 return (
  <div className="flex flex-col items-center justify-center min-h-screen space-y-4">
    <input
      type="file"
      multiple
      accept=".txt"
      onChange={handleChange}
      className="text-center"
    />
    <button
      onClick={handleUpload}
      className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
    >
      Test Sliding Window
    </button>
  </div>
);

};

export default SlidingWindow;
