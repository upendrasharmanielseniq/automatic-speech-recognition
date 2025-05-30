// PredictButton.jsx
import React from 'react';

const PredictButton = ({ onPredict, isDisabled }) => {
  return (
    <button
      onClick={onPredict}
      disabled={isDisabled}
      className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
    >
      Predict
    </button>
  );
};

export default PredictButton;
