import React from 'react';

const ListenButton = ({ onFileSelect }) => {
  const handleChange = (e) => {
    if (e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="flex justify-center mb-4">
      <label className="cursor-pointer bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded">
        Upload Transcript
        <input
          type="file"
          accept=".txt"
          onChange={handleChange}
          className="hidden"
        />
      </label>
    </div>
  );
};

export default ListenButton;
