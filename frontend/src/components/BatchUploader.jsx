import React, { useState } from 'react';
import { uploadBatchTranscripts } from '../services/api';

const BatchUploader = () => {
    const [files, setFiles] = useState([]);

    const handleChange = (e) => {
        setFiles(Array.from(e.target.files));
    }
    
    const handleUpload = async () => {
        try {
            const response = await uploadBatchTranscripts(files);
            const blob = new Blob([response.data], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'predictions.csv';
            link.click();
        } catch (error) {
            console.error('Error uploading files:', error);
            alert('Failed to upload files. Please try again.');
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
      Batch Predict
    </button>
  </div>
);

};

export default BatchUploader;
